from lexer import lexer


def test_string_with_spaces():
    tokens = lexer('bta "Enter number: " integer a\n')
    assert any(t[0] == 'STRING' and t[1] == 'Enter number: ' for t in tokens)


def test_string_preserve_underscore():
    tokens = lexer('laao "math_utils"\n')
    assert any(t[0] == 'STRING' and t[1] == 'math_utils' for t in tokens)


def test_list_literal_spaces():
    tokens = lexer('maan lo nums hai [1, 2, 3]\n')
    assert any(t[0] == 'LIST' and t[1] == [1, 2, 3] for t in tokens)


def test_list_literal_no_spaces():
    tokens = lexer('maan lo nums hai [1,2,3]\n')
    assert any(t[0] == 'LIST' and t[1] == [1, 2, 3] for t in tokens)


def test_multi_word_keyword_for():
    tokens = lexer('har ek n nums me\n    chhaap n\n')
    assert any(t[0] == 'FOR' for t in tokens)
