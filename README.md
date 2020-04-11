# MinewaysToRenderman
Maya Python script to convert [Mineways](http://www.realtimerendering.com/erich/minecraft/public/mineways/)-provided Phong shaders into PxrSurface shaders for use with Renderman.
Instantly setup your imported worlds for rendering with Renderman!

Tested on Maya 2019 with Renderman 23.1

## Setup
Extract the Mways_to_Rman folder into your Maya script directory. Drag the "run.py" into the script editor's Python tab, then select the snippet and middle-click drag it into a shelf of your choice. Save your shelf when done.

Or just install it like you normally would with your other custom scripts I guess.

## Usage
### Export
Export your model from Mineways using "Export for Rendering". I personally use these settings. Results may vary depending on your export configuration.

![Mineways Settings Image](https://i.imgur.com/mZCXa9K.png)

### Import
Import the model into Maya, select all the transform nodes for each of the block types you want to convert. Click the shelf button to begin the process.

## Contributing
If you want to help, feel free to submit a PR! If you run into an issue, create one.

## Author
This is my first open-source repo, please be gentle!

Check out my website and other stuff at https://blocker226.design/
