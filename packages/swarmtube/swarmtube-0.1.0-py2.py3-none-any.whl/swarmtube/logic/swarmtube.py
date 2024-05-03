"""Main module."""

# library modules
import asyncio
import random
import time
import functools
from typing import Callable, List, Dict, Any
from pydantic import BaseModel

from agptools.progress import Progress


# ---------------------------------------------------------
# local imports
# ---------------------------------------------------------
# from ..helpers import expandpath

# ---------------------------------------------------------
# models / mappers
# ---------------------------------------------------------
# from ..models.swarmtube import SwarmtubeApp
# from .. import mappers
# from ..models.enums import *
# from ..definitions import TAG_KEY

# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------

from agptools.logs import logger

log = logger(__name__)

"""
USE NS test DB test;
INFO FOR NS;
INFO FOR DB;
--SELECT * FROM bigplanner_models_inventory_PlannerItem;
--SELECT COUNT() FROM person GROUP ALL;
-- SELECT * FROM person LIMIT 1;
-- SELECT * FROM clock ORDER BY _wave ASC LIMIT 1000;
-- SELECT * FROM clock WHERE _wave > 0 ORDER BY _wave ASC LIMIT 2;
--SELECT * FROM random_plus_one;
-- DELETE FROM clock, random_plus_one, _waves;
--SELECT _wave, payload FROM random_plus_one ORDER BY _wave ASC;
SELECT * FROM _waves;
--SELECT math::max(random_plus_one._wave);
-- RETURN math::max([SELECT random_plus_one["_wave"] FROM random_plus_one]);
SELECT COUNT() FROM clock GROUP ALL;
SELECT COUNT() FROM random_plus_one GROUP ALL;
"""


UID = str
WAVE = float


class Event(BaseModel):
    "TBD"
    wave: WAVE
    uid: UID
    payload: Any = None


class Storage:
    """Abstract Interface for Storage"""

    def __init__(self):
        pass

    async def start(self):
        "any action related to start storage operations"

    async def stop(self):
        "any action related to stop storage operations"

    async def last_wave(self, uid: UID) -> WAVE:
        "Get the last wave for a given uid"

    async def get(self, uid: UID, wave: WAVE, max_results=1000) -> List[Event]:
        "get data order than the given wave (i.e. > wave)"

    def put(self, uid: UID, edge):
        "put data into storage"


class Broker:
    "Basic Broker capabilities"

    def __init__(self):
        self.subscriptions: Dict[UID, List[Callable]] = {}

    async def start(self):
        "any action related to start broker operations"

    async def stop(self):
        "any action related to stop broker operations"

    async def subscribe(self, uid: UID, callback: Callable):
        "TBD"
        inventory = self.subscriptions.setdefault(uid, [])
        if callback not in inventory:
            inventory.append(callback)

    async def unsubscribe(self, uid: UID, callback: Callable):
        "TBD"
        inventory = self.subscriptions.setdefault(uid, [])
        if callback in inventory:
            inventory.remove(callback)


class iAgent(object):
    def __init__(self, uid, broker: Broker, storage: Storage, meta=None, *args, **kw):
        self.uid = uid
        self.broker = broker
        self.storage = storage

        self.state = ST_INIT
        self.meta = {} if meta is None else meta
        super().__init__(*args, **kw)

    async def main(self):
        "main loop"
        # await super().main()
        await self._start_live()
        while self.state < ST_STOPPED:
            await self._idle()
        await self._stop_live()

    async def _start_live(self):
        log.info("[%s] _start_live", self.uid)

    async def _stop_live(self):
        log.info("[%s] _stop_live", self.uid)

    async def _idle(self):
        log.info("[%s] alive", self.uid)
        await asyncio.sleep(2)


class Tube(iAgent):
    """Represents the concept of a stream of events that
    can be located by a UID or searching metadata
    """

    uid: UID

    def __init__(
        self, uid: UID, sources: List[UID], broker: Broker, storage: Storage, meta=None
    ):
        super().__init__(uid=uid, broker=broker, storage=storage, meta=meta)
        self.sources = sources


class App(iAgent):
    "TBD"

    def __init__(self, uid='app', *args, **kw):
        super().__init__(uid=uid, *args, **kw)
        self.tubes = {}
        self.tasks = {}
        self.loop = None
        self.t0 = 0

    async def _start_live(self):
        assert self.loop is None
        self.loop = asyncio.get_running_loop()
        self.t0 = self.loop.time()

        # start broker and storage
        await self.storage.start()
        await self.broker.start()

        # start tubes
        for uid, tube in self.tubes.items():
            log.info("- starting: [%s]", uid)
            self.tasks[uid] = self.loop.create_task(tube.main(), name=uid)

    async def _stop_live(self):
        # requests fibers to TERM
        for uid, tube in self.tubes.items():
            log.info("- term: [%s]", uid)
            tube.state = ST_STOPPED

        # wait and clear stopped
        t0 = self.loop.time()
        while self.tasks and self.loop.time() - t0 < 5:
            for uid, task in list(self.tasks.items()):
                if task.done():
                    self.tasks.pop(uid)
                    log.info("- end: [%s]", uid)
            await asyncio.sleep(0.5)

        # kill remaining
        for uid, task in self.tasks.items():
            log.info("- kill: [%s]", uid)
            task.cancel()

        t0 = self.loop.time()
        while self.tasks and self.loop.time() - t0 < 5:
            for uid, task in list(self.tasks.items()):
                if task.done():
                    self.tasks.pop(uid)
                    log.info("- finished: [%s]", uid)
            await asyncio.sleep(0.5)

        # stop broker and storage
        await self.storage.stop()
        await self.broker.stop()

    def must_stop(self):
        return False

    def add(self, *tubes):
        for tube in tubes:
            self.tubes[tube.uid] = tube

    def run(self):
        asyncio.run(self.main())

    async def _idle(self):
        await super()._idle()
        if self.must_stop():
            self.state = ST_STOPPED
            log.info("[%s] want stop", self.uid)


ST_INIT = 0
ST_HISTORICAL = 1
ST_SWITCHING = 2
ST_LIVE = 3
ST_STOPPED = 4


class Clock(Tube):
    "A tube that emit a clock tick"
    counter: int

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.counter = 0

    async def _start_live(self):
        await super()._start_live()

    async def _stop_live(self):
        await super()._stop_live()

    async def _idle(self):
        await super()._idle()
        self.counter += 1
        edge = {
            "_wave": time.time(),  # TODO: let the storage set this value?
            #'uid': uid,
            "payload": self.counter,
        }
        self.storage.put(self.uid, edge)


class Particle(Tube):
    "TBD"
    MAX_EVENTS = 1024
    buffer = Dict[UID, List[Event]] | None
    _historical = Dict[UID, List[Event]] | None

    def __init__(self, uid: UID, sources: List[UID], broker: Broker, storage: Storage):
        super().__init__(uid, sources=sources, broker=broker, storage=storage)
        # self.uid = uid
        # self.sources = sources
        # self.broker = broker
        # self.storage = storage
        self.wave0 = {}
        self.buffer = {}
        self._historical = {}
        self._need_resync = False
        self._milk = []
        self.metrics = Progress()
        for uid in self.sources:
            self.buffer[uid] = []
            self._historical[uid] = []

    async def main(self):
        "TBD"
        self._need_resync = True
        # self.metrics.start()
        while self._need_resync:
            self._need_resync = False
            await self._start_live()
            await self._start_historical()

        log.info("=" * 70)
        log.info("[%s] >> Idle", self.uid)
        log.info("=" * 70)

        while self.state < ST_STOPPED:
            await asyncio.sleep(2)
            self.metrics.update(n=0)

        await self._stop_live()

    async def _start_live(self):
        "TBD"
        log.info("[%s] ++ Requesting LIVE STREAMING", self.uid)

        for uid in self.sources:
            await self.broker.subscribe(uid, self.live)

    async def _stop_live(self):
        "TBD"
        for uid in self.sources:
            await self.broker.unsubscribe(uid, self.live)

    async def _start_historical(self):
        "TBD"
        self.state = ST_HISTORICAL
        _wave = await self.storage.last_wave(self.uid)
        self.wave0 = {uid: _wave for uid in self.sources}
        buffer = self._historical
        self._milk = list(self.sources)
        log.info("-" * 70)
        log.info("[%s] -- Switching to HISTORICAL", self.uid)
        log.info("-" * 70)
        while self.state < ST_LIVE:
            # load some historical data
            n = 0
            while self._milk:
                uid = self._milk.pop()
                data = await self.storage.get(
                    uid, self.wave0[uid], max_results=self.MAX_EVENTS
                )
                if data:
                    buffer[uid].extend(data)
                    n += len(data)
                    self.wave0[uid] = data[-1]["_wave"]
                    break

            if n == 0:  # no more historical data
                # move live data to historical and try to continue until
                # we get a state with no more historical data and no more live data
                self.state = ST_SWITCHING
                # time.sleep(0.9)
                assert id(buffer) != id(self.buffer)
                for uid, _buff in self.buffer.items():
                    _hist = self._historical[uid]
                    while True:
                        try:
                            candidate = _buff.pop(0)
                            if candidate["_wave"] > self.wave0[uid]:
                                _hist.append(candidate)
                                n += 1
                            else:
                                # this live event has been captured by historical polling
                                # so is already processed
                                # print(f"*** already processed: --> {candidate}")
                                foo = 1
                        except IndexError:
                            break
                if n == 0:
                    log.info("*" * 70)
                    log.info("[%s] ** Switching to LIVE STREAMING **", self.uid)
                    log.info("*" * 70)
                    self.metrics.update(n=0, force=True)
                    self.state = ST_LIVE

            # try to process buffer
            while self.state < ST_LIVE:
                _uid, _wave, edge = self.pop_edge(buffer)
                if edge:
                    self.dispatch(edge)
                    if not buffer[uid]:  # request more data
                        self._milk.append(_uid)
                elif self.state == ST_SWITCHING:
                    break
                else:
                    break  # continue loading more historical
            # check if we have an overflow while processing historical data
            if self._need_resync:
                log.info(
                    "[%s] *** ---> Request Stopping Streaming due OVERFLOW", self.uid
                )
                await self._stop_live()

    def live(self, uid: UID, event: Dict):
        "TBD"
        if len(self.buffer[uid]) >= self.MAX_EVENTS:
            self._need_resync = True
            return
        self.buffer[uid].append(event)
        if self.state == ST_LIVE:
            # try process events until the edge is incomplete
            while True:
                _uid, _wave, edge = self.pop_edge(self.buffer)
                if edge:
                    self.dispatch(edge)
                    self.wave0[_uid] = _wave
                else:
                    assert not all(
                        self.buffer.values()
                    ), "some input must be missing here!"
                    break
        elif len(self.buffer[uid]) >= self.MAX_EVENTS:
            # request stop streaming and a new re-sync process
            self._need_resync = True

    def pop_edge(self, buffer):
        "analyze buffer and return edge if all data is available for processing next step"
        # TODO: implement a policy delegation criteria to know when edge is ready to be processed
        waves = {}
        for uid, data in buffer.items():
            if data:
                waves[uid] = data[0]["_wave"]

        # have we all needed data?
        if len(waves) == len(self.sources):
            _uid, _wave, edge = self._pop_policy(buffer, waves)
            self.wave0[_uid] = _wave
            return _uid, _wave, edge
        return None, None, None

    def _pop_policy(self, buffer, waves):
        """Default policy is to make the minimal step for computation.
        - get the minimal wave
        - drop the input related with the minimal wave
        - return a custom `edge` for computation
        """
        edge = {}
        _wave = min(waves.values())
        for uid, data in buffer.items():
            item = data[0]
            if _wave == item["_wave"]:
                data.pop(0)
                _uid = uid
            edge[uid] = item

        edge["_wave"] = _wave
        return _uid, _wave, edge

    def dispatch(self, edge):
        "TBD"
        # build the data to be processed
        ikeys = set([k for k in edge if k.startswith("_")])
        ekeys = ikeys.symmetric_difference(edge)
        assert ekeys, "no payload in the edge?"
        data = {k: edge[k] for k in ikeys}

        # do the computation
        data["payload"] = self._compute(edge, ekeys)

        # store results
        self.storage.put(self.uid, data)
        N = sum([len(_) for _ in self.buffer.values()])
        self.metrics.update(buffer=N)

        log.info(f"[%s] -> dispatch: %s", self.uid, edge)
        log.info(f"[%s] <- dispatch: %s", self.uid, data)

    def _compute(self, edge, ekeys):
        raise NotImplementedError()


# ---------------------------------------------------------
# Surreal Implementation
# ---------------------------------------------------------
from surrealist import Surreal


class Subscription(BaseModel):
    lq_uid: UID
    callbacks: List[Callable]


class SurrealBroker(Broker):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self._live_queries = {}
        self.surreal = Surreal(
            # "http://localhost:9000",
            self.url,
            namespace="test",
            database="test",
            credentials=("root", "root"),
            use_http=False,
            timeout=10,
            log_level="ERROR",
        )
        log.info(
            self.surreal.is_ready()
        )  # prints True if server up and running on that url
        log.info(self.surreal.version())  # prints server version
        self.connection = self.surreal.connect()

    async def subscribe(self, uid: UID, callback: Callable):
        "TBD"
        await super().subscribe(uid, callback)
        conn = self.connection
        lq = self._live_queries.get(uid)
        if lq:
            lq.callbacks.append(callback)
        else:
            handler = functools.partial(self.dispatch, uid)
            res = conn.live(uid, callback=handler)
            lq_uid = res.result
            lq = self._live_queries[uid] = Subscription(
                lq_uid=lq_uid, callbacks=[callback]
            )

    def dispatch(self, uid: str, res):
        "process an event from broker"
        result = res["result"]
        assert result["action"] in ("CREATE",)
        # event = Event(uid=uid, **result['result'])
        event = result["result"]
        for callback in self._live_queries[uid].callbacks:
            callback(uid, event)

    async def unsubscribe(self, uid: UID, callback: Callable):
        "TBD"
        await super().unsubscribe(uid, callback)
        conn = self.connection
        lq = self._live_queries.get(uid)
        if lq:
            lq.callbacks.remove(callback)
            if not lq.callbacks:
                conn.kill(lq.lq_uid)
                self._live_queries.pop(uid)
        else:
            pass


class SurrealStorage(Storage):
    "Surreal storage implementation"

    def __init__(self, url):
        self.url = url
        self.surreal = Surreal(
            # "http://localhost:9000",
            self.url,
            namespace="test",
            database="test",
            credentials=("root", "root"),
            use_http=False,
            timeout=1000,
            log_level="ERROR",
        )
        self.connection = None

    async def start(self):
        "any action related to start storage operations"
        self.connection = self.surreal.connect()

    async def stop(self):
        "any action related to stop storage operations"
        self.connection.close()

    async def get(self, uid: UID, wave: WAVE, max_results=1000) -> List[Event]:
        "get data older than wave (i.e. > wave)"
        query = f"""
        SELECT *
        FROM {uid}
        WHERE  _wave > {wave}
        ORDER BY _wave ASC
        LIMIT {max_results}
        """
        # if not self.connection.is_connected():
        # foo = 1
        res = self.connection.query(query)
        return res.result

    async def last_wave(self, uid: UID) -> WAVE:
        "TBD"
        res = self.connection.select(f"_waves:{uid}")
        result = res.result
        if result:
            return result[0]["_wave"]
        return 0

    def put(self, uid: UID, edge):
        "put data"
        # insert data into database
        self.connection.create(uid, edge)

        # update known last wave for this particular uid
        data = {"_wave": edge["_wave"]}
        res = self.connection.update(f"_waves:{uid}", data)
        return res.result


# ---------------------------------------------------------
# Example of a Particle Implementation
# ---------------------------------------------------------
class PlusOne(Particle):
    def _compute(self, edge, ekeys):
        s = 0
        for k in ekeys:
            s += edge[k]["payload"]

        s /= len(ekeys)
        s += random.random()
        return s


class TempDiff(Particle):
    def _compute(self, edge, ekeys):
        X = [edge[k]["payload"] for k in ekeys]
        y = X[0] - X[-1]
        return y
