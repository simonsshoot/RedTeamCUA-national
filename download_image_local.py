#!/usr/bin/env python3
"""
Download VM Image Script for RedTeamCUA
This script downloads the pre-built VM image from OSWorld for local use.
"""

import os
import platform
import logging
from desktop_env.providers.vmware.manager import VMwareVMManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Download the appropriate VM image based on the current platform.
    """
    logger.info("Starting VM image download for RedTeamCUA...")
    
    # Determine OS type based on platform
    if platform.system() == 'Darwin':  # macOS
        os_type = "Ubuntu"
        logger.info(f"Detected macOS system, downloading Ubuntu ARM image...")
    elif platform.system() in ['Windows', 'Linux']:
        if platform.machine().lower() in ['amd64', 'x86_64']:
            os_type = "Ubuntu" 
            logger.info(f"Detected {platform.system()} x86_64 system, downloading Ubuntu x86 image...")
        else:
            logger.error(f"Unsupported architecture: {platform.machine()}")
            return
    else:
        logger.error(f"Unsupported operating system: {platform.system()}")
        return
    
    try:
        # Create VMware VM Manager
        vm_manager = VMwareVMManager()
        
        # Set VM directory
        vms_dir = "./vmware_vm_data"
        
        logger.info(f"VM will be installed to: {vms_dir}")
        
        # Get VM path (this will download if not exists)
        vm_path = vm_manager.get_vm_path(os_type=os_type, region=None)
        
        logger.info("✅ VM image download completed successfully!")
        logger.info(f"VM location: {vm_path}")
        
    except Exception as e:
        logger.error(f"❌ Failed to download VM image: {str(e)}")
        logger.error("Please check your internet connection and try again.")
        raise

if __name__ == "__main__":
    main()