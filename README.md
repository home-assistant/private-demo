# Private demo

This builds an image that has the demo integartion setup
This is used for app verification and deployed with https://github.com/home-assistant/deployments


## Updates

- To change the configuration the instance is using, adjsut the [`rootfs/etc/config/configuration.yaml`](./rootfs/etc/config/configuration.yaml) file.
- To change the version of Home Assistant that is used, adjust the first file in the [`Dockerfile`](./Dockerfile) file.

After a change is merged, create a release of the repository to publish a new image. When the image is publised the [deployment can be updated](https://github.com/home-assistant/deployments/blob/main/private_demo/main.tf).
