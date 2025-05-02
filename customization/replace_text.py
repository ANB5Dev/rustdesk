#!/usr/bin/env python3

import os
import sys
import re
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "customization"))
from generate_custom_text import process_diff, process_diffs

if __name__ == "__main__":
    
    print('Applying ANB5 edits\n')

    diffs = [

        # Make empty peer list less dramatic
        {
            'file': 'flutter/lib/common/widgets/peers_view.dart',
            'from': 'Icons.sentiment_very_dissatisfied_rounded,',
            'to':   'Icons.computer_rounded,'
        },

        # Don't show "setup your own server" tip
        {
            'file': 'flutter/lib/desktop/pages/connection_page.dart',
            'from': 'if (!isIncomingOnly) setupServerWidget(),'
        },

        # Remove 'powered by' message on desktop
        {
            'file': 'flutter/lib/desktop/pages/desktop_home_page.dart',
            'from':
'''\
      if (bind.isCustomClient())
        Align(
          alignment: Alignment.center,
          child: loadPowered(context),
        ),
'''
        },

        # Uncheck 'Install {} Printer' by default
        {
            'file': 'flutter/lib/desktop/pages/install_page.dart',
            'from': "printer.value = installOptions['PRINTER'] != '0'",
            'to':   "printer.value = '0' != '0'"
        },

        # Remove unused options in settings menu
        {
            'file': 'flutter/lib/desktop/pages/desktop_setting_page.dart',
            'multi': [
                {   # account tab in settings (doesn't work on server)
                    'from': '    if (!bind.isDisableAccount()) SettingsTabKey.account,'
                },
                {   # ID card in settings (doesn't work on server)
                    'from': "                _Card(title: 'ID', children: [changeId()]),"
                },
            ]
        },

        # AGPL attribution and source code link
        {
            'file': 'flutter/lib/desktop/pages/desktop_setting_page.dart',
            'from':
'''\
              InkWell(
                  onTap: () {
                    launchUrlString('https://rustdesk.com/privacy.html');
                  },
                  child: Text(
                    translate('Privacy Statement'),
                    style: linkStyle,
                  ).marginSymmetric(vertical: 4.0)),
              InkWell(
                  onTap: () {
                    launchUrlString('https://rustdesk.com');
                  },
                  child: Text(
                    translate('Website'),
                    style: linkStyle,
                  ).marginSymmetric(vertical: 4.0)),
''',
            'to':
'''\
              InkWell(
                  onTap: () {
                    launchUrlString(
                        'https://www.gnu.org/licenses/agpl-3.0.html');
                  },
                  child: Text(
                    translate('License'),
                    style: linkStyle,
                  ).marginSymmetric(vertical: 4.0)),
              InkWell(
                  onTap: () {
                    launchUrlString('https://github.com/ANB5Dev/rustdesk/');
                  },
                  child: Text(
                    translate('Source'),
                    style: linkStyle,
                  ).marginSymmetric(vertical: 4.0)),
'''
        },

        # Remove slogan
        {
            'file': 'flutter/lib/desktop/pages/desktop_setting_page.dart',
            'from':
'''\
                          Text(
                            translate('Slogan_tip'),
                            style: TextStyle(
                                fontWeight: FontWeight.w800,
                                color: Colors.white),
                          )
'''
        },

        # Don't show scam warning on mobile
        {
            'file': 'flutter/lib/mobile/pages/server_page.dart',
            'from': 'bind.mainGetLocalOption(key: "show-scam-warning")',
            'to':   '"N"',
            'times': 2
        },

        # Remove 'powered by' message on mobile
        {
            'file': 'flutter/lib/mobile/pages/settings_page.dart',
            'from':
'''\
        if (bind.isCustomClient())
          Align(
            alignment: Alignment.center,
            child: loadPowered(context),
          ),
'''
        },

        # Hide account section in mobile app (only works on pro server)
        {
            'file': 'flutter/lib/mobile/pages/settings_page.dart',
            'from': 'if (!bind.isDisableAccount())',
            'to':   'if (false)'
        },

        # Hide tabs 4 and 5 (they require login, available on pro only)
        {
            'file': 'flutter/lib/models/peer_tab_model.dart',
            'from': 'static const int maxTabCount = 5;',
            'to':   'static const int maxTabCount = 3;'
        },

        # Remove excess languages
        {
            'file': 'src/lang.rs',
            'multi': [
                 {
                    'from': 'mod ar;.*?mod vn;',
                    'to':   'mod en;\nmod nl;',
                    'regex': True,
                    'regex_flags': re.DOTALL
                 },
                 {
                    'from': 'pub const LANGS: .*?];',
                    'to':   'pub const LANGS: &[(&str, &str)] = &[\n    ("en", "English"),\n    ("nl", "Nederlands"),\n];',
                    'regex': True,
                    'regex_flags': re.DOTALL
                 },
                 {
                    'from': r'let m = match lang\.as_str\(\) {.*?};',
                    'to':
'''\
let m = match lang.as_str() {
        "nl" => nl::T.deref(),
        _ => en::T.deref(),
    };
''',
                    'regex': True,
                    'regex_flags': re.DOTALL
                 }
            ]  
        },

        # Always replace "RustDesk" by custom app name, even if it contains 'RustDesk'
        {
            'file': 'src/lang.rs',
            'from': 'if s.contains("RustDesk")',
            'to':   'if true'
        },

        # Change texts
        {
            'file': 'src/lang/en.rs',
            'multi': [
                {
                    'from': '("ID/Relay Server", "ID/Relay server"),',
                    'to':   '("ID/Relay Server", "Alternative ID/Relay server"),'
                },
                {
                    'from': r'\("empty_recent_tip", ".*?"\),',
                    'to':   '("empty_recent_tip", "No recent sessions."),',
                    'regex': True
                },
                {
                    'from': r'\("empty_favorite_tip", ".*?"\),',
                    'to':   '("empty_favorite_tip", "No favourite peers yet."),',
                    'regex': True
                },
                {
                    'from': r'\("empty_lan_tip", ".*?"\),',
                    'to':   '("empty_lan_tip", "No peers detected on this LAN."),',
                    'regex': True
                },
                {
                    'from': r'\("upgrade_rustdesk_server_pro_to_{}_tip", ".*?"\),',
                    'to':   '("upgrade_rustdesk_server_pro_to_{}_tip", "This feature is not yet supported."),',
                    'regex': True
                },
                {
                    'from': r'\("id_input_tip", ".*?"\),',
                    'to':   r'("id_input_tip", "You can input an ID, a direct IP, or a domain with a port (<domain>:<port>).\\n\\nIf you want to access a device on another server, please append the server address and key (<id>@<server_address>?key=<key_value>), for example:\\n9123456234@192.168.16.1:21117?key=5Qbwsde3unUcJBtrx9ZkvUmwFNoExHzpryHuPUdqlWM="),',
                    'regex': True
                },
                {
                    'from': r'\("web_id_input_tip", ".*?"\),',
                    'to':   r'("web_id_input_tip", "You can input an ID in the same server, direct IP access is not supported in web client.\\n\\nIf you want to access a device on another server, please append the server address and key (<id>@<server_address>?key=<key_value>), for example:\\n9123456234@192.168.16.1:21117?key=5Qbwsde3unUcJBtrx9ZkvUmwFNoExHzpryHuPUdqlWM="),',
                    'regex': True
                },
            ]
        },

        {
            'file': 'src/lang/nl.rs',
            'multi': [
                {
                    'from': 'Bureaublad',
                    'to': 'Apparaat',
                    'times': 3
                },
                {
                    'from': 'bureaublad',
                    'to': 'apparaat',
                    'times': 8
                },
                {
                    'from': 'Apparaatpictogram',
                    'to': 'Bureaubladpictogram'
                },
                {
                    'from': 'Snelkoppeling op apparaat maken',
                    'to': 'Snelkoppeling op bureaublad maken'
                },
                {
                    'from': 'ID-/Relayserver',
                    'to': 'Alternatieve ID-/Relayserver'
                },
                {
                    'from': r'\("empty_recent_tip", ".*?"\),',
                    'to':   '("empty_recent_tip", "Geen recente sessies."),',
                    'regex': True
                },
                {
                    'from': r'\("empty_favorite_tip", ".*?"\),',
                    'to':   '("empty_favorite_tip", "Nog geen favoriete apparaten."),',
                    'regex': True
                },
                {
                    'from': r'\("empty_lan_tip", ".*?"\),',
                    'to':   '("empty_lan_tip", "Nog geen apparaten ontdekt op dit LAN."),',
                    'regex': True
                },
                {
                    'from': r'\("upgrade_rustdesk_server_pro_to_{}_tip", ".*?"\),',
                    'to':   '("upgrade_rustdesk_server_pro_to_{}_tip", "Deze functionaliteit is nog niet ondersteund."),',
                    'regex': True
                },
                {
                    'from': r'\("id_input_tip", ".*?"\),',
                    'to':   r'("id_input_tip", "U kunt een ID, een direct IP of een hostname met poort (<hostname>:<poort>) invoeren.\\n\\nAls u toegang wilt tot een apparaat op een andere server, voeg dan een serveradres en public key toe (<id>@<server_adres>?key=<key_value>), bijvoorbeeld:\\n9123456234@192.168.16.1:21117?key=5Qbwsde3unUcJBtrx9ZkvUmwFNoExHzpryHuPUdqlWM="),',
                    'regex': True
                },
                {
                    'from': r'\("web_id_input_tip", ".*?"\),',
                    'to':   r'("web_id_input_tip", "U kunt een ID invoeren op dezelfde server, directe IP-toegang wordt niet ondersteund in de webclient.\\n\\nAls u toegang wilt tot een apparaat op een andere server, voegt u het serveradres en public key toe (<id>@<server_adres>?key=<key_value>), bijvoorbeeld:\\n9123456234@192.168.16.1:21117?key=5Qbwsde3unUcJBtrx9ZkvUmwFNoExHzpryHuPUdqlWM="),',
                    'regex': True
                },
            ]
        },
        
        # Make Windows installer work for apps with spaces
        {
            'file': 'src/platform/windows.rs',
            'multi': [
                {
                    'from': r'(^\s*|")(reg|sc) (\S+) (\S+)',
                    'to':   r'\1\2 \3 \\"\4\\"',
                    'times': 47,
                    'regex': True,
                    'regex_flags': re.MULTILINE
                },
                {
                    'from': r'reg add HKEY_CLASSES_ROOT\\.{ext}',
                    'to': r'reg add \"HKEY_CLASSES_ROOT\.{ext}\"'
                },
                {
                    'from': 'taskkill /F /IM {broker_exe}',
                    'to':   'taskkill /F /IM \\"{broker_exe}\\"',
                    'times': 2
                },
                {
                    'from': 'taskkill /F /IM {app_name}.exe{filter}',
                    'to':   'taskkill /F /IM \\"{app_name}.exe\\"{filter}',
                    'times': 3
                },
                {
                    'from': 'taskkill /F /IM {}',
                    'to':   'taskkill /F /IM \\"{}\\"'
                },
                {
                    'from': 'taskkill /F /IM {process_exe}',
                    'to':   'taskkill /F /IM \\"{process_exe}\\"'
                },
                {
                    'from': 'let size = meta.len() / 1024;',
                    'to':   'let size = 54080;'
                }
            ]
        },

    ]

    error_count = process_diffs(diffs)
    print(f'done! errors: {error_count}\n')

    print('The following files (might) have been changed:')
    print(' '.join([d['file'] for d in diffs]))

    if error_count:
        sys.exit(1)