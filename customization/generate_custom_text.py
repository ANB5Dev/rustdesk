#!/usr/bin/env python3

import sys
import json
import re
from datetime import datetime
from types import SimpleNamespace

def main():

    if len(sys.argv) < 2:
        print(r"Usage: python generate_icons.py '<JSON>', eg:")
        print('python generate_custom_text.py \'{ \\"app_name\\": \\"ASCI Hulp op Afstand\\", \\"email\\": \\"info@asci.nl\\", \\"description\\": \\"ASCI Hulp op Afstand Remote Desktop Application\\", \\"company\\": \\"ASCI Technologies BV\\", \\"website\\": \\"https://asci.nl\\", \\"privacy_url\\": \\"https://asci.nl\\", \\"identifier\\": \\"nl.asci.hulpopafstand\\", \\"copyright\\": \\"ASCI Technologies BV\\", \\"images\\": \\"asci\\", \\"incoming_only\\": true, \\"debug\\": true }\'')
        sys.exit(1)

    config_arg = sys.argv[1]
    config_dict = json.loads(config_arg)
    print('config:')
    print(config_dict)
    config = SimpleNamespace(**config_dict)

    print('Adding custom texts\n')


    diffs = [

        # NB: "RustDesk" in src/lang/*.rs wordt at runtime vervangen in src/lang.rs: s.replace("RustDesk", &crate::get_app_name());

        # Rust project metadata
        {
            'file': 'Cargo.toml',
            'multi': [
                {
                    'from': 'authors = ["rustdesk <info@rustdesk.com>"]',
                    'to':  f'authors = ["{config.company} <{config.email}>"]'
                },
                {  
                    'from': '"RustDesk Remote Desktop"',
                    'to':  f'"{config.description}"',
                    'times': 2
                },
                {
                    'from': r'LegalCopyright = "Copyright © \d+ Purslane Ltd\. All rights reserved\."',
                    'to':   f'LegalCopyright = "Copyright © {datetime.now().year} Purslane Ltd. & {config.copyright}. All rights reserved."',
                    'regex': True
                },
                {
                    'from': '"RustDesk"',
                    'to':  f'"{config.app_name}"',
                    'times': 2
                },
                {
                    'from': 'com.carriez.rustdesk',
                    'to':   config.identifier
                },
            ]
        },

        # Rust<->Flutter bridge
        {
            'file': 'flutter/lib/web/bridge.dart',
            'from': "return 'RustDesk';",
            'to':  f"return '{config.app_name}';"
        },

        # Enable incoming-only mode
        {
            'file': 'libs/hbb_common/src/config.rs',
            'if':   config.incoming_only,
            'from':
'''\
pub fn is_incoming_only() -> bool {
    HARD_SETTINGS
        .read()
        .unwrap()
        .get("conn-type")
        .map_or(false, |x| x == ("incoming"))
}
''',
            'to':
'''\
pub fn is_incoming_only() -> bool {
    true
}
'''
        },

        # Common code

        {
            'file': 'build.py',
            'from': "system2('cp -rf ../target/release/service ./build/macos/Build/Products/Release/RustDesk.app/Contents/MacOS/')",
            'to':  f"system2('cp -rf ../target/release/service \"./build/macos/Build/Products/Release/{config.app_name}.app/Contents/MacOS/')\""
        },

        {
            'file': 'libs/hbb_common/src/config.rs',
            'multi': [
                {
                    'from': '"RustDesk"',
                    'to':  f'"{config.app_name}"'
                },
                {
                    'from': '"rs-ny.rustdesk.com"',
                    'to':   f'"{config.server}"'
                },
                {
                    'from': '"OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw="',
                    'to':  f'"{config.pubkey}"'
                }
            ]
        },

        {
            'file': 'src/main.rs',
            'multi': [
                {
                    'from': '.author("Purslane Ltd<info@rustdesk.com>")',
                    'to':  f'.author("{config.company}<{config.email}>")'
                },
                {
                    'from': '.about("RustDesk command line tool")',
                    'to':  f'.about("{config.app_name} command line tool")'
                }
            ]
        },

        {
            'file': 'flutter/lib/desktop/widgets/tabbar_widget.dart',
            'from': '"RustDesk",',
            'to':  f'"{config.app_name}",'
        },

        {
            'file': 'src/auth_2fa.rs',
            'from': 'const ISSUER: &str = "RustDesk";',
            'to':  f'const ISSUER: &str = "{config.app_name}";'
        },

        {
            'file': 'flutter/lib/desktop/pages/desktop_setting_page.dart',
            'from': 'Purslane Ltd.\\n$license',
            'to':  f'Purslane Ltd. & {config.copyright}.\\n\\nThis program is based on work originally created by Purslane Ltd. and has been adapted by {config.copyright}.\\n\\nThis program is distributed under the terms of the GNU Affero General Public License (AGPL), version 3 or later, as published by the Free Software Foundation. You may redistribute and/or modify this software under the terms of the AGPL. See the AGPL for more details.'
        },

        # Enable debug output for windows cmds
        {
            'file': 'src/platform/windows.rs',
            'if':   config.debug,
            'from':
'''\
fn run_cmds(cmds: String, show: bool, tip: &str) -> ResultType<()> {
''',
            'to':
'''\
fn run_cmds(cmds: String, show: bool, tip: &str) -> ResultType<()> {

    let cmds = format!("{}\\npause", cmds);
    let show = true;
'''
        },

        # Windows self-extracting exe
        {
            'file': 'libs/portable/Cargo.toml',
            'multi': [
                {
                    'from': 'description = "RustDesk Remote Desktop"',
                    'to':  f'description = "{config.description}"'
                },
                {
                    'from': r'LegalCopyright = "Copyright © \d+ Purslane Ltd\. All rights reserved\."',
                    'to':   f'LegalCopyright = "Copyright © {datetime.now().year} Purslane Ltd. & {config.copyright}. All rights reserved."',
                    'regex': True
                },
                {
                    'from': 'ProductName = "RustDesk"',
                    'to':  f'ProductName = "{config.app_name}"'
                },
                {
                    'from': 'FileDescription = "RustDesk Remote Desktop"',
                    'to':  f'FileDescription = "{config.description}"'
                }
            ]
        },

        # Windows installer
        {
            'file': 'flutter/lib/desktop/pages/install_page.dart',
            'from': 'https://rustdesk.com/privacy.html',
            'to':    config.privacy_url,
            'times': 2
        },

        # Windows runner
        {
            'file': 'flutter/windows/runner/Runner.rc',
            'multi': [
                {
                    'from': 'Purslane Ltd',
                    'to':   config.company,
                    'times': 2
                },
                {
                    'from': 'VALUE "FileDescription", "RustDesk Remote Desktop" "\\0"',
                    'to':  f'VALUE "FileDescription", "{config.description}" "\\0"'
                },
                {
                    'from': 'VALUE "ProductName", "RustDesk" "\\0"',
                    'to':  f'VALUE "ProductName", "{config.app_name}" "\\0"'
                }
            ]
        },

        # macOS AppInfo
        {
            'file': 'flutter/macos/Runner/Configs/AppInfo.xcconfig',
            'multi': [
                {
                    'from': 'PRODUCT_NAME = RustDesk',
                    'to':  f'PRODUCT_NAME = {config.app_name}'
                },
                {
                    'from': 'PRODUCT_COPYRIGHT = Copyright © 2025 Purslane Ltd. All rights reserved.',
                    'to':  f'PRODUCT_COPYRIGHT = Copyright © 2025 Purslane Ltd. & {config.copyright}. All rights reserved.'
                }
            ]
        },

    ]

    error_count = process_diffs(diffs)
    print(f'done! errors: {error_count}')
    if error_count:
        sys.exit(1)


def process_diff(file, diff):
    '''
    diff = { from, to = '', times = 1, if = True, regex = False, regex_flags = 0 }
    '''
    diff_from = diff['from']
    diff_to = diff.get('to', '')
    diff_times = diff.get('times', 1)
    diff_if = diff.get('if', True)
    if isinstance(diff_if, str) and diff_if.lower() in ['false', '0']:
        diff_if = False
    diff_regex = diff.get('regex', False)
    diff_regex_flags = diff.get('regex_flags', 0)

    print(f'{file}:', end=' ')

    if not diff_if:
        print('condition not met, skipping\n')
        return 0

    with open(file, 'r', encoding='utf8') as infile:
        content = infile.read()

    if diff_regex:
        content, count = re.subn(diff_from, diff_to, content, flags=diff_regex_flags)
    else:
        count = content.count(diff_from)
        content = content.replace(diff_from, diff_to)

    with open(file, 'w', encoding='utf8') as outfile:
        outfile.write(content)

    print(f'replaced {count}/{diff_times} times:')
    if diff_regex:
        print(f'(regex enabled, flags: {diff_regex_flags})')
    print('\t'+'\n\t'.join(diff_from.splitlines()))
    print('\t=>')
    print('\t'+'\n\t'.join(diff_to.splitlines()))

    if diff_times != count:
        print("┌──────────────────────────────────────────┐")
        print("│ ERROR: incorrect number of replacements! │")
        print("└──────────────────────────────────────────┘")

    print()

    return abs(count - diff_times)


def process_diffs(diffs):
    '''Handle "multi" '''
    error_count = 0
    for d in diffs:
        file = d['file']
        if 'multi' in d:
            for d in d['multi']:
                error_count += process_diff(file, d)
        else:
            error_count += process_diff(file, d)
    return error_count


if __name__ == "__main__":
    main()