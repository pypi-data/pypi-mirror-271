import os
from code_to_text.code_to_text import read_ignore_patterns, is_ignored

def test_read_ignore_patterns(tmpdir):
    p = tmpdir.join("test_ignore.txt")
    p.write(".git\n*.log\n")

    expected_patterns = ['.git', '*.log']
    patterns = read_ignore_patterns(str(p))
    assert patterns == expected_patterns

def test_is_ignored():
    ignore_patterns = ['.git', '*.log', 'node_modules']
    root = '/path/to/project'
    assert is_ignored('.git', ignore_patterns, root)
    assert is_ignored('logs/error.log', ignore_patterns, root)
    assert not is_ignored('src/index.js', ignore_patterns, root)
