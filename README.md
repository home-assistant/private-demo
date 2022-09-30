# Private demo

This builds an image that has the [demo](https://www.home-assistant.io/integrations/demo/) integrations enabled.
This is used for app verification and deployed with https://github.com/home-assistant/deployments


## Updates

- To change the configuration which is used by the instance, adjust the [`rootfs/etc/config/configuration.yaml`](./rootfs/etc/config/configuration.yaml) file.
- To change the version of Home Assistant that is used, adjust the first line in the [`Dockerfile`](./Dockerfile) file.

After a change is merged, create a release of the repository to publish a new image. After the image is published, the [deployment can be updated](https://github.com/home-assistant/deployments/blob/main/private_demo/main.tf).
