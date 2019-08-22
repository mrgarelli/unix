#!/usr/bin/env python3

from syspy import parseOptions, fail, succeed, getInputs, Shell, error, os
sh = Shell()

version = 'Version: 1.0'

shortcuts = {
	'a': ['add'],
	'aa': ['add', '.'],
	'b': ['branch'],
	'c': ['commit'],
	'ca': ['commit', '--amend'],
	'ch': ['checkout'],
	'i': ['init'],
	'l': ['log'],
	'm': ['merge'],
	'ph': ['push'], 
	'pho': ['push', 'origin'],
	'pl': ['pull'],
	'plr': ['pull', '--rebase'],
	'plo': ['pull', 'origin'],
	'rma': ['rm', '-r', '--cached', '.'],
	'rst': ['reset'],
	'rsth': ['reset', '--hard', 'HEAD'],
	's': ['status'],
	'sh': ['stash'],
	'shc': ['stash', 'clear'],
	't': ['ls-tree', '-r', '--name-only'],
	}

help_msg = '''options
	-h, --help :\thelp menu
	-p :\t\tplatform specific tracker (linux, osx)
	-u :\t\tunix configuration tracker
	-v, --verbose :\tlist the actual command being run
	--version :\tversion

command shortcuts'''

def help():
	print(help_msg)
	for sh in shortcuts:
		print('\t', sh, ':\t', ' '.join(shortcuts[sh]))

unix = False
platform = False
verbose = False

git_command = '/usr/bin/git'
command_with_tree = [
	git_command,
	' --work-tree=',
	sh.home
	]
unix_git_command = ''.join(
	command_with_tree + [' --git-dir=', sh.home, '/.unx']
	)
platform_git_command = ''.join(
	command_with_tree + [' --git-dir=', sh.home, '/.pltfrm']
	)

shortOpts = 'hpuv'
longOpts = [
	'help',
	'verbose',
	'version',
	]

# parsed options and gathers remainder (command)
options, command, remainder = parseOptions(getInputs(), shortOpts, longOpts)

# deals with options accordingly
for opt, arg in options:
	if opt in ('-h', '--help'):
		help()
		succeed()
	elif opt in ('-p'):
		platform = True
		git_command = platform_git_command
	elif opt in ('-u'):
		unix = True
		git_command = unix_git_command
	elif opt in ('-v', '--verbose'):
		verbose = True
		sh.verbose = True
	elif opt == '--version':
		print(version)
		succeed()

def git(command):
	sh.command([git_command] + command)

def add_all(files):
	files = [sh.home + f for f in files]
	for file in files:
		git(['add', file])

def add_all_unix_files():
	files = [
		'/.bashrc',
		'/.gitignore',
		'/readme.md',
		'/.settings/*',
		'/scripts/src/*',
		'/scripts/scripts.py',
		'/Local/scripts.py',
		]
	add_all(files)

def add_all_platform_files():
	platform = os()
	if platform == 'linux':
		files = [
			'/.vimrc',
			'/.profile',
			'/.xinitrc',
			'/.inputrc',
			'/.local/share/konsole/*',
			'/.config/konsolerc',
			'/.config/Code/User/keybindings.json',
			'/.config/Code/User/settings.json',
			'/.config/openbox/lxde-rc.xml',
			]
	elif platform =='mac':
		files = [
			'/.vimrc',
			'/.profile',
			'/Library/Application\ Support/Code/User/keybindings.json',
			'/Library/Application\ Support/Code/User/settings.json',
		]
	else:
		error('unrecognized platform')
	add_all(files)

if (command):
	if command == 'aa':
		if unix: add_all_unix_files()
		elif platform: add_all_platform_files()
		else: git(['add .'])
	else:
		git(shortcuts.get(command, [command]) + remainder)
else:
	# default behavior of the package
	help()
	# git(['']) # calls the default git help
