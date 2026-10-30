import asyncio
import json
import sys

import pytest

from . import disteval, disteval_benchmark


@pytest.mark.parametrize('fail', [False, True])
def test_disteval_without_current_loop(monkeypatch, capsys, fail):
    asyncio.set_event_loop(None)
    monkeypatch.setattr(sys, 'argv', ['disteval', 'integral.json', '--format=json'])
    monkeypatch.setattr(disteval, 'load_worker_commands', lambda *args: [['worker']])
    prepared = object()
    loops = []
    result = {'regulators': ['eps'], 'sums': {}, 'integrals': {}}

    async def prepare(*args):
        loops.append(asyncio.get_running_loop())
        return prepared

    async def evaluate(state, *args):
        assert state is prepared
        loops.append(asyncio.get_running_loop())
        await asyncio.sleep(0)
        if fail:
            raise RuntimeError('evaluation failed')
        return result

    async def clear(state):
        assert state is prepared
        loops.append(asyncio.get_running_loop())

    monkeypatch.setattr(disteval, 'prepare_eval', prepare)
    monkeypatch.setattr(disteval, 'do_eval', evaluate)
    monkeypatch.setattr(disteval, 'clear_eval', clear)

    if fail:
        with pytest.raises(RuntimeError, match='evaluation failed'):
            disteval.main()
    else:
        disteval.main()
        assert json.loads(capsys.readouterr().out) == result

    assert len(loops) == 3
    assert all(loop is loops[0] for loop in loops)
    assert loops[0].is_closed()


def test_benchmark_without_current_loop(monkeypatch, capsys):
    asyncio.set_event_loop(None)
    monkeypatch.setattr(sys, 'argv', ['disteval_benchmark', 'integral.json'])
    loops = []

    async def benchmark(*args):
        loops.append(asyncio.get_running_loop())
        await asyncio.sleep(0)
        print('family,kernel,rate,rate_error')

    monkeypatch.setattr(disteval_benchmark, 'dobenchmark', benchmark)
    disteval_benchmark.main()

    assert capsys.readouterr().out == 'family,kernel,rate,rate_error\n'
    assert len(loops) == 1
    assert loops[0].is_closed()
