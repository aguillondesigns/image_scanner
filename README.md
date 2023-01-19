# Python Image Scanning API using Google Vision
Very simple API that allows the end user to supply base64 image data or a an image url which can use the Google Vision API to perform object detection. 

## Build Instructions
Before you get started, there are a few files that need tweaking.
    
### Docker Compose Setup
`docker-compose.yml` There is an example file `docker-compose.yml.example` located in the root of this repo. You will want to modify the environment variables for each of the services, namely:

- [x] MYSQL_ROOT_PASSWORD
- [x] VISION_APIKEY
- [x] DB_USER
- [x] DB_PASSWORD

The other environment variables in the file should be left alone as they are specific to the code and compose file.

### Kubernets Setup
`secret.yml` There is an example file `secret.yml.example` located in the root of this repo. The are only a few secrets needed here and they are already mapped in the needed deployment files:

- [x] db_user
- [x] db_password
- [x] vision_apikey

 We are using secrets of type `data` and they should be base64 encoded before placed in this file.

`scanner-db-deployment.yml` This file is pretty much already setup, but there is one item that we need to adjust. We are using the `hostPath` method for volume storage which is pointing to a physical location on the node. Kubernetes supports a slew of different [volumes](https://kubernetes.io/docs/concepts/storage/volumes/) for you to use. For the sake of simplicity, we are using a local storage path of `C:\coding\local_volume`, please note the structure of the path in the yaml file: `/run/desktop/mnt/host/c/coding/local_volume` the **/run/desktop/mnt/host** is needed for this to work.

### Container Creation
Now that you have the your `docker-compose.yml` or your `secret.yml` configured, you are ready to roll.

You will find two scripts `build.bat` (Windows) and `build.sh` (Linux variants).  These are designed to be run from inside your `image_scanner` directory. For the `build.sh` you will want to enable script execution for it to work correctly: ```sudo chmod +x build.sh```

Once both of the containers have been built, you will be ready launch the app.

## Deployment
All the hard work is done, deployment is cake!

**Docker Compose** - while inside `image_scanner`, type: `docker compose up -d` . The `-d` flag allows compose to start up in detached mode (container are running in the background). To bring the the containers down, type: `docker compose down` while inside the `image_scanner` directory.

**Kubernetes** - while inside `image_scanner\kubernetes`, type: `kubectl apply -f .` . To bring the pods/services down, use `kubectl delete -f .` while inside the `image_scanner\kubernetes` directory.

## Usage Examples
Depending on your deployment you will be using different sets of ports: 

**Docker Compose** uses `localhost:5000` for the api and `localhost:8080` for phpmyadmin.

**Kubernetes** uses `locahost:30000` for the api and `localhost:30001` for phpmyadmin.

**Note** - The db port 3306 is exposed locally for Docker Compose, but it does not have a node port assigned for the Kubernetes setup.

### Get Requests
Response Structure:
```json
{
    "id" : 1,
    "image" : "base 64 encoded image data",
    "objects" : "comma,separated,values,for,searching",
    "title" : "title supplied or generated",
    "use_detection" : true
}
```

- `localhost:[port]/images` - Returns all available images
- `localhost:[port]/images/[id]` - Returns a specific image
- `localhost:[port]/images?objects=cat,dog` - Returns all images where objects supplied are found

### Post Requests
Request Structure:
```json
{
    "title" : "cute kitten",
    "use_detection" : false,
    "url" : "https://wallpaperstock.net/wallpapers/thumbs1/36793hd.jpg",
    "image" : "base 64 encoded image data"
}
```
The post request supports 4 parameters, but only one of (`url` or `image`) is required. `title` will be populated based on google vision properties or, if detection is disabled, will be a generic title using the image id. `use_detection` allows you to send images to the api without triggering the [Google Vision API](https://cloud.google.com/vision). If both the `url` and `image` params are supplied, the system will use the `image` contents.

### Enjoy!
