"""Dependency-isolated reachability regression tests; no packets are sent."""
import ast
import errno
import ipaddress
from pathlib import Path
import shutil
import subprocess
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

SOURCE = Path(__file__).resolve().parents[1] / 'app/services/nmap_scanner.py'
node = next(n for n in ast.parse(SOURCE.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'ping_host')
ns = {'ip_in_authorized_scope': lambda ip: ipaddress.ip_address(ip).is_private,
      'ipaddress': ipaddress, 'shutil': shutil, 'subprocess': subprocess}
exec(compile(ast.Module(body=[node], type_ignores=[]), str(SOURCE), 'exec'), ns)
ping_host = ns['ping_host']


def test_icmp_timeout_uses_linux_seconds():
    with patch('shutil.which', return_value='/bin/ping'), patch('subprocess.run', return_value=SimpleNamespace(returncode=0)) as run:
        assert ping_host('192.168.1.2')[0]
        assert run.call_args.args[0][-2:] == ['2', '192.168.1.2']


def probe(result, ip='192.168.1.2'):
    sock = MagicMock()
    sock.__enter__.return_value = sock
    sock.connect_ex.return_value = result
    with patch('shutil.which', return_value=None), patch('socket.socket', return_value=sock) as factory:
        up, latency = ping_host(ip)
    assert sock.__exit__.called
    return up, latency, factory


def test_open_port_is_reachable():
    assert probe(0)[0]


def test_refused_port_is_reachable():
    assert probe(errno.ECONNREFUSED)[0]


def test_timeout_is_not_online():
    assert probe(errno.ETIMEDOUT)[:2] == (False, None)


def test_no_route_is_not_online():
    assert not probe(errno.EHOSTUNREACH)[0]


def test_ipv6_socket_family():
    import socket
    assert probe(0, 'fd00::2')[2].call_args.args[0] == socket.AF_INET6


def test_out_of_scope_does_not_probe():
    with patch('socket.socket') as sock, patch('subprocess.run') as run:
        assert ping_host('8.8.8.8') == (False, None)
        sock.assert_not_called()
        run.assert_not_called()
