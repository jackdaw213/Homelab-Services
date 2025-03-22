## Proxmox Host Configuration

### Run Essential Scripts
Execute the following commands on the Proxmox host:
```bash
bash -c "$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/misc/microcode.sh)"
bash -c "$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/misc/scaling-governor.sh)" - schedutil
bash -c "$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/misc/post-pve-install.sh)"
```

### Add Proxmox Node to Netdata
Ensure the Proxmox node is monitored by Netdata.

---

## Arch Linux VM Configuration

### Virtual Machine Settings
- **BIOS**: OVMF (UEFI)
- **Machine Type**: Q35
- **Root Disk**: 80GB
- **CPU Type**: Host
- **RAM**: 18GB

### Adding an EFI Disk and Boot Option
Follow the [guide here](#) to add an EFI disk and configure boot options.

### Disk Configuration
To list available disk IDs:
```bash
ls -n /dev/disk/by-id/
```
To attach a disk to VM (replace `*X*` and `*disk id*` accordingly):
```bash
/sbin/qm set 100 -virtio*X* /dev/disk/by-id/*disk id*
```

### GPU Passthrough (NVIDIA P600)
Add the NVIDIA P600 as a raw PCIe device with all functions passed through.

### Docker Network Setup
Create a new Docker network with a specified subnet:
```bash
docker network create --subnet=172.18.0.0/16 main_net
```

### Permissions Configuration
Set proper permissions to avoid issues:
```bash
sudo chmod 755 /mnt/lab_data/
```
More details on permissions: [MergerFS Discussion](https://github.com/trapexit/mergerfs/discussions/1253)

