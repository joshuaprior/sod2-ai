> [!IMPORTANT]
> The commit that introduces this document marks the start of a large reimplementation of the synth data generation tool. The tool will be broken until the reimplemetantion is complete.

# Reimplement Synth Data Generation

## Background
The first attempt at training the model to recognize SOD2 base facilities worked a little, however I quickly realized that the model was using the positions in the image to determine if a specific facility was selected. When I moved the workshop to a new location the model could no longer recognize when the workshop was selected.

This is when I decided to try training the model with synthetic data. It was practically impossible to train the model to look for all possible base configurations using real game screenshots. Obtaining those screenshot would take months to collect because I would need to create communities in every possible zone, aquire every possible base, and configure it with every possible facility in every possible orientation. 

## CURRENT STATE
### Features
#### Noisy background
The background is a noisy image (screen capture from game play) that forces the model to ignore anthing that isn't the facility icons and the selection rectangle that indicates which one is selected.

#### Random Placement
The facility icons that are added to the image are placed in random locations within the synth frame. This should force the model to learn that the facility icon can appear anywhere on the screen.

#### Random Visability
For *workshop* labled frames the workshop will always be visible and selected. Every other facility only has a 50% chance of being included in the frame. This is to train the model that the workshop can be selected even if the other facilities are not present on the screen. This is importnat to support all possible base configurations where the player may select from an assortment of faciliteis to populate the base.

### Failures
#### Icon Dimensions
I discovered that the facility icons that I downloaded from the community wiki can not be scaled to the correct size to match what the UI renders in the game. This is becuse they were rendered onto the brown paper texture with the wrong relative demensions between the icon and the background.

#### Selection Opacity
In the game the selection rectangle has an animated opacity that pulses to make the selection fade in an out. The opacity seems to range from about 20% to 100%. So in the synth data the opacity is applied to the selection rectangle as well. However, the synth data has a very noisy background and I think that the randomness of the colors whent the opacity is very low causes the model to get confused about what facility icon is selected.

#### Generation Efficency
In order to get an antialiased look for the icon and the selection rectangle I chose to render the frame at 4x resolution then scale it down to the target resolution. This is a pretty heavy operation and makes the frames take a long time to render. Which makes it harder to iterate on ideas to improve the synth data. Right now it takes about an hour to generate 2,000 frmaes of synth training data, and the images consume about 20GB of drive space.

## Target State
The next synth data implementation will build off of the knowledge gained in the previous implementation, with some tweaks to, hopefully, make the model perform better.

### Features to keep
- Noisy background
- Random placement
- Random visiblity

### Features to add
#### Accurate Icons
I found modding tools that allowed me to extract the games visual assets. I was able to get the actual icon images used by the game to render the facility icons. They are black with a transparent background. They will need to be scaled to fit the dimensions of the icons in the game. I have not been able to find the background image that the game renders behind the icons, but I'm sure it must be in the game assets somewhere. I think it is important to include the background because otherwise the icons will blend too much with the noisy background and the model will not be able to identify which icon is which.

### Temporal Selection Detection
To avoid the model getting confused when the selection rectangle is very low opacity, I plan to only create training data that has the selection opacity between 80% and 100%. During the inference phase I expect that the model will only be able to detect the selection when the opacity of the selection rectantle is very high. So to correct for this I will grab multiple frmaes during the time it takes the opacity to cycle once. If any of the frames are detected as a selection then I will consider the menu to be selected.

### Remove Super Res Rendering
I think I can get the same antialiasing look while rendering at the target resolution for the frame. To achive this I plan on rendering the selection rectangle and all the facility icons at super resolution on a transparent background, down sampling them to the target resolution, then save the images to the drive. To generate synth data these new antialiased images will be loaed and pasted into a frame that is at the target resolution. The alpha blending should take care of the antialias effect. This will reduce the amount of time it takes to render one frame of synth data.

### Apply Transform Pipeline Before Writing To Disk
The current synth data is stored as 2560x1440 images, which matches the target resolution for the game. However, during training these images get resied to 224x224 before feeding them to the model. It will save gigabytes of space if I apply the model transform pipeline before saving the image to disk. There are a bunch of benefits from this change. Primarily the saved disk space, but also the model training should go faster because the images will already be in the correct format. Additionally I think that even the synth data generation might be faster because there will be less time spent waiting for the drive to allocate space and write data.

### Optimization to Research
I think that if I apply the model transform pipeline to all of the assets that compose the image before composing them then I can just paste together frames from 224x224 scaled backgrounds, facility icons, and selection rectangle. This would avoid any resizing during the generation of synth frames and should drop the time to generate even further. I will lose some of my ability to position the facility icons, but if the result is a model that can better detect selections then the loss doesn't matter.

## Rough Breakdown of Work
- Decompose data generation tool into several smaller modules so the AI can make small targeted chnages without trying to rewrite the whole system on every prompt.
- Generate the antialiased transparency assets for the selection rectangle, facility icons, and the brown icon background.
- Reimplement the data generation tool to render images at the target resolution of 2560x1440 with no super resolution rendering.
- Refactor the data generation tool to apply the model transform pipeline before storing the frame to disk.

