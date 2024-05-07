"""Test Proem class."""
from contextlib import nullcontext as does_not_raise

import pytest
from colorama import Fore

# from contextlib import nullcontext as does_not_raise
from src.proem import Proem

RESET = Fore.RESET

template = {
    "app_nm": "test-app",
    "flavor_text": None,
    "version": None,
    "repo_url": None,
    "width": 80,
    "border_char": "#",
    "border_color": "magenta",
    "description": None,
    "description_align": "left"
}

@pytest.mark.parametrize('class_args, expected_except', [
    # test app_nm only
    (template, does_not_raise()),
    # test app_nm and flavor_text
    (template | {'flavor_text': 'A test application'}, does_not_raise()),
    # test app_nm, flavor_text, and version
    (template | {'flavor_text': 'A test application', 'version': 'v1.0.0'}, does_not_raise()),
    # test app_nm, flavor_text, version, and repo_url
    (template | {'flavor_text': 'A test application', 'version': 'v1.0.0', 'repo_url': 'https://github.com'}, does_not_raise()),
    # test app_nm, flavor_text, version, repo_url, and description
    (template | {'flavor_text': 'A test application', 'version': 'v1.0.0', 'repo_url': 'https://github.com', 'description': 'A long description'}, does_not_raise()),
    # test app_nm, flavor_text, version, repo_url, description, and description_align = right
    (template | {'flavor_text': 'A test application', 'version': 'v1.0.0', 'repo_url': 'https://github.com', 'description': 'A long description', 'description_align': 'right'}, does_not_raise()),
    # test app_nm, flavor_text, version, repo_url, description, and description_align = center
    (template | {'flavor_text': 'A test application', 'version': 'v1.0.0', 'repo_url': 'https://github.com', 'description': 'A long description', 'description_align': 'center'}, does_not_raise()),
    # test different width
    (template | {'width': 40}, does_not_raise()),
    # test width smaller than app_nm length
    (template | {'width': len(template['app_nm']) - 1}, does_not_raise()),
    # test width of 0
    (template | {'width': 0}, does_not_raise()),
    # test width of 1000
    (template | {'width': 1000}, does_not_raise()),
    # test different border_char = *
    (template | {'border_char': '*'}, does_not_raise()),
    # test multiple border_char = **
    (template | {'border_char': '**'}, does_not_raise()),
    # test app_nm, flavor_text, version, repo_url, description, and description_align = center
    (template | {'flavor_text': 'A test application', 'version': 'v1.0.0', 'repo_url': 'https://github.com', 'border_char': '**',  'description': 'A long description'}, does_not_raise()),
    # test border_color = red
    (template | {'border_color': 'red'}, does_not_raise()),
    # test border_color that is not supported
    (template | {'border_color': 'notasupportedcolor'}, does_not_raise()),
    # test bad description
    (template | {'description': 'A long description', 'description_align': 'bad'}, pytest.raises(ValueError)),
])

def test_build_func(class_args, expected_except):
    """Test Proem build function."""
    with expected_except:
        p = Proem(
            class_args['app_nm'],
            class_args['flavor_text'],
            class_args['version'],
            class_args['repo_url'],
            class_args['width'],
            class_args['border_char'],
            class_args['border_color'],
            class_args['description'],
            class_args['description_align']
        )

        build_text = p.build()

        color = ''

        if class_args['border_color'] == 'magenta':
            color = Fore.MAGENTA
        elif class_args['border_color'] == 'red':
            color = Fore.RED

        border = color + class_args['border_char'] * p.width + RESET
        sborder = color + class_args['border_char'] + RESET

        lines = [(class_args['app_nm'], 'center')]

        if class_args['flavor_text']:
            lines.append((class_args['flavor_text'], 'center'))

        if class_args['version']:
            lines.append(('', 'center'))
            lines.append((class_args['version'], 'center'))

        if class_args['repo_url']:
            lines.append(('', 'center'))
            lines.append((class_args['repo_url'], 'center'))

        if class_args['description']:
            lines.append(('', 'center'))
            lines.append((class_args['description'], class_args['description_align']))

        expected_build_text = [border]

        empty_width = p.width - 2

        for l, a in lines:
            if l and a == 'center':
                expected_build_text.append(sborder + l.center(empty_width * len(p.border_char)) + sborder)
            elif l and a == 'left':
                expected_build_text.append(sborder + ' ' + l.ljust(empty_width * len(p.border_char) - 1) + sborder)
            elif l and a == 'right':
                expected_build_text.append(sborder + l.rjust(empty_width * len(p.border_char) - 1) + ' ' + sborder)
            else:
                expected_build_text.append(sborder + ' ' * empty_width * len(p.border_char) + sborder)

        expected_build_text.append(border)

        # Convert to a string with newlines
        expected_build_text = '\n'.join(expected_build_text) + '\n'

        print(build_text)
        print(expected_build_text)

        assert build_text == expected_build_text

def test_bad_align():
    """Test Proem _text_line function with bad align."""
    with pytest.raises(ValueError):
        p = Proem('test-app')

        p._text_line('test', 'bad_align') # pylint: disable=protected-access
