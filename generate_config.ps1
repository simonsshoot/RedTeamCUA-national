# RedTeamCUA Configuration Generation Script for Windows
# Equivalent to generate_config.sh

Write-Host "=== Generating RedTeamCUA Configurations ===" -ForegroundColor Green

# Remove existing configuration files
Write-Host "Cleaning up existing configuration files..." -ForegroundColor Yellow
if (Test-Path "evaluation_examples/test_all_owncloud.json") { Remove-Item "evaluation_examples/test_all_owncloud.json" }
if (Test-Path "evaluation_examples/test_all_reddit.json") { Remove-Item "evaluation_examples/test_all_reddit.json" }
if (Test-Path "evaluation_examples/test_all_rocketchat.json") { Remove-Item "evaluation_examples/test_all_rocketchat.json" }

Write-Host "Generating normal configurations..." -ForegroundColor Yellow

# OwnCloud configurations
Write-Host "Generating OwnCloud configurations..." -ForegroundColor Cyan
python generate_config.py --benign_task_raw "goals/benign/benign_task.raw_own_owncloud_setup_project.json" --adversary_task_raw "goals/adv/adversary_task.raw_own_owncloud_setup_project.json" --output_path "evaluation_examples"
python generate_config.py --benign_task_raw "goals/benign/benign_task.raw_own_owncloud_linux_tutorial.json" --adversary_task_raw "goals/adv/adversary_task.raw_own_owncloud_linux_tutorial.json" --output_path "evaluation_examples"
python generate_config.py --benign_task_raw "goals/benign/benign_task.raw_own_owncloud_docker_entry.json" --adversary_task_raw "goals/adv/adversary_task.raw_own_owncloud_docker_entry.json" --output_path "evaluation_examples"

# Reddit configurations
Write-Host "Generating Reddit configurations..." -ForegroundColor Cyan
python generate_config.py --benign_task_raw "goals/benign/benign_task.raw_own_reddit_gitclone.json" --adversary_task_raw "goals/adv/adversary_task.raw_own_reddit_gitclone.json" --output_path "evaluation_examples"
python generate_config.py --benign_task_raw "goals/benign/benign_task.raw_own_reddit_alias_tmux.json" --adversary_task_raw "goals/adv/adversary_task.raw_own_reddit_alias_tmux.json" --output_path "evaluation_examples"
python generate_config.py --benign_task_raw "goals/benign/benign_task.raw_own_reddit_install_termcolor.json" --adversary_task_raw "goals/adv/adversary_task.raw_own_reddit_install_termcolor.json" --output_path "evaluation_examples"

# RocketChat configurations
Write-Host "Generating RocketChat configurations..." -ForegroundColor Cyan
python generate_config.py --benign_task_raw "goals/benign/benign_task.raw_own_rocketchat_git_config.json" --adversary_task_raw "goals/adv/adversary_task.raw_own_rocketchat_git_config.json" --output_path "evaluation_examples"
python generate_config.py --benign_task_raw "goals/benign/benign_task.raw_own_rocketchat_install_nodejs.json" --adversary_task_raw "goals/adv/adversary_task.raw_own_rocketchat_install_nodejs.json" --output_path "evaluation_examples"
python generate_config.py --benign_task_raw "goals/benign/benign_task.raw_own_rocketchat_vim_editor.json" --adversary_task_raw "goals/adv/adversary_task.raw_own_rocketchat_vim_editor.json" --output_path "evaluation_examples"

Write-Host "=== Configuration Generation Complete! ===" -ForegroundColor Green
Write-Host "Configuration files have been generated in the 'evaluation_examples' directory." -ForegroundColor Cyan
