# Optical Simulation SDK
## Begin

Our optical simulation SDK is released in a beta version and has only limited features support at the moment.
We are working on supporting more features and you can expect new versions to come out soon.

#### Install

The python package installation is available using PyPi:

```bash
pip install threed-optix
```

#### Get your API key

Get your API key from 3DOptix user interface (under "user settings"):

- Click on your email in the top right corner, and choose **"user settings"** in the drop-down
  ![User settings](https://i.yourimageshare.com/MyBdTqNzyQ.webp "User settings")
- On the buttom of the user settings manu, click on **"API"**
  ![API settings](https://i.yourimageshare.com/IbcB26QfJh.webp "API settings")
- **Copy** your API key
  ![Get API key](https://i.yourimageshare.com/tPq7LC8Qfy.webp "Get API key")

#### Start

`tdo.Client` object is used to communicate with 3DOptix databases and simulation engine.

```python
import threed_optix as tdo

#Your API key from 3DOptix user interface
api_key = '<your_api_key>'

#api is the object that manages the communication with 3DOptix systems
client = tdo.Client(api_key)
```

## Basics

### Setups

`tdo.Setup` are the objects that represent your simulation setups in the SDK.
You could access their information:

- `setup.name` is the setup name. It is not neceseraliy unique.
- `setup.id` is the id of the setup. It is unique.
- `setup.parts` is a list of `tdo.Part` objects that the setup contains.

#### Create a `tdo.Setup`

You could create a new setup with `client.create_setup` method. The method has the following arguments:
- `name`: str, The name of the setup.
- `description`: str, The description of the setup.
- `labels`: list[str], the labels of the setup. Can be anything from `tdo.SETUP_LABELS`.
- `units`: str, 'mm' or 'inch'. Default to 'mm'.
- `private`: bool, `True` for private setup and `False` for a public one. Default to `False`.

```python
setup = client.create_setup(name = name,
                            description = description,
                            labels = labels,
                            private = True)
```

#### Find a setup:

First, we need to identify the setup we want to work on:

```python
#Examine the setups:
for setup in client:
    print(setup.name, setup.id)
```

> **Note**
> A setup id is unique, but the name is not unique

Then, we can get the setup object by using `client.get(name)` and `client[id]` methods:

```python
#Get setup by name
setup_name = '<your setup name>'
setup = client.get(setup_name)

#Get setup by id
setup_id = '<your setup id'
setup = client[setup_id]
```

### Parts:

`tdo.Part` are the objects that represent your setup parts in the SDK.
You could access their information:

- `part.label` is the label of the part. It is not neceseraliy unique.
- `part.id` is the id of the setup. It is unique.
- `part.surfaces` is a list of `tdo.Surface` objects that the part has.
- `part.pose` is a list of 6 floats representing the part's position and rotation relative to their associated coordinate system.

> **Warning**
> Setups with parts that were loaded from a CAD file are not supported fully at the moment.
> These CAD parts will not lead to an error, but they might lead to unexpected behavior.

`tdo.Detector` is the object used to represent detectors. It inherits all properties and functionalities from `tdo.Part` while also introducing specific attributes tailored for representing detectors within the SDK.
`tdo.Detector` has the following additional information:

- `detector.size`
- `detector.opacity`

`tdo.LightSource` is the object used to represent light sources. It inherits all properties and functionalities from `tdo.Part` while also introducing specific attributes tailored for representing light sources within the SDK.
`tdo.LightSource` has the following additional information:

- `ls.wavelengths`
- `ls.power`
- `ls.rays_direction`
- `ls.vis_count`
- `ls.count_type`
- `ls.opacity`
- `ls.color`
- `ls.source_type`
- And information that changes with respect to `source_type`.

`tdo.Optic` is the object used to represent optics. It inherits all properties and functionalities from `tdo.Part` while also introducing specific attributes tailored for representing optics within the SDK.
`tdo.Optic` has the following additional information:
- `part.db_id` is the id of the part in our database (not in the setup). For example, two lenses in the setup can be the same database object. They will have different ids, but the same db_id.
- `part.optical_data` contains all the data that's specific to the optical properties of the part, such as its geometry, shape, brand, physical data, etc.


**You could see a full description of these objects, as well as how to modify them, later on this document**.

#### Add a `tdo.Part`:
To add a detector to the setup:
```python
detector = setup.add_detector(**kwargs)
```

To add a light source to the setup:
```python
ls = setup.add_light_source(**kwargs)
```

To add optic to the setup, we will have to find its `db_id` from the product catalog or take the number id of the created optic from `client.create_xxx` methods.
```python
ls = setup.add_optics(db_id = db_id,
                      **kwargs)
```
You could get the part number id in the `ID` column in the product catalog, or take the number id of the part you created.

>> **Note**
>> You can add parts with any keyword arguments from part.change_config to add and change properties with the same command.

#### Find a part:

Almost identical to finding a setup.

```python
#Examine the parts of the setup
for part in setup:
    print(part.label, part.id)
```

> **Note**
> A part id is unique, but the label is not unique

Then, we can identify the part and start working, similarly to how we identified the setup:

```python
#Get part by label
part_label = '<your part label>'
part = setup.get(part_label)

#Get part by id
part_id = '<your part id'
part = setup[part_id]
```

If the part is not found, `setup[part_id]` **will** lead to an error, and `setup.get(part_label)` will **not**.

#### Delete a part from the setup:
In order to remove a part from the setup, we simply use `setup.delete_part` method as follows:
```python
part_to_delete = setup.get('<part_to_delete_label>')
setup.delete_part(part_to_delete)
```
And that's it! The part is removed from the setup.

### Surface

`tdo.Surface` are the objects that represent the surfaces of the part in the SDK.
You could access their information:

- `surface.name` is the name of the surface. It is not neceseraliy unique.
- `surface.id` is the id of the setup. It is unique.
- If the surface is the front of a detector, you could access the analyses with `surface.analyses`. It is a list of `tdo.Analysis` objects that the surface has. Later on we discuss how to create, find and run them.

#### Create or add a `tdo.Surface`

Creation of new surfaces is not possible.

#### Find a surface:

Almost identical to finding your setups and parts within your setups.

```python
for surface in part:
    print(surface.name, surface.id)
```

Then, we can identify the surface by `part.get()` and `part[]` methods:

```python
#Get surface by name
surface_name = '<your surface name>'
surface = part.get(surface_name)

#Get surface by id
surface_id = '<your surface id>'
surface = part[surface_id]
```

### Scattering
Each surface of `tdo.Optic` part can have scattering properties.
To examine them, check `surface.scattering` property.
If the surface does not have scattering, it will return `False`.
#### Disable Surface Scattering
If a surface has a scattering that you want to disable, simply use `surface.disable_scattering` method.
```python
surface.diasble_scattering()
if not surface.scattering:
    print('Success!')
```
#### Add Or Change Scattering
Scattering can be added or changed with `surface.XXX_scattering` methods.
Each of them acccepts the following arguments:
- `transmittance`, `absorption`, `reflection`: float, The proportion of  the light that is transmitted, absorbed and reflected by the surface.
- `split_ratio`: int, number of ray that each ray split to.
- `power_threshold`: float, Relative power threshold used for terminating the ray tracing simulation. It represents the minimum amount of remaining power below which rays are terminated.

##### Cos-nth
Requires also `n` parameter, which defaults to 1.5.
```python
surface.cos_scattering(transmittance = 0.5,
                        reflection = 0.3,
                        absorption = 0.1,
                        split_ratio = 10,
                        power_threshold = 5,
                        n = 2)
```
##### Gaussian
Requires also `sigma_x`, `sigma_y` and `azimuth_theta` parameters.
```python
surface.gaussian_scattering(transmittance = 0.99,
                            reflection = 0.01,
                            absorption = 0,
                            split_ratio = 5,
                            power_threshold = 2
                            sigma_x = 10,
                            sigma_y = 15,
                            azimuth_theta = 0)
```

##### ABG
Requires also `a`, `b` and `g` parameters.
```python
surface.abg_scattering(transmittance = 0.95,
                            reflection = 0.025,
                            absorption = 0.025,
                            split_ratio = 7,
                            power_threshold = 4
                            a = 1,
                            b = 2,
                            g = 2)
```

##### Lambertian
Does not require unique parameters.
```python
surface.lambartian_scattering(transmittance = 0.97,
                            reflection = 0.03,
                            absorption = 0.01,
                            split_ratio = 10,
                            power_threshold = 5,
                            )
```

### Coordinate Systems
#### Part Coordinate System
You can see all of the coordinate systems that a part has in `part.cs` list.
Every `CoordinateSystem` object has `name`, `pose`, and `id` properties.
The local coordinate system is accesible with `part.lcs`, and the reference coordinate system is accesible with `part.rcs` (with the relevant part).
```python
for cs in part.cs:
    print(cs.name, cs.id, cs.pose)

lcs = part.lcs
rcs, reference_part = part.rcs
```
#### The World Coordinate System
The world coordinate system is stored in `tdo.GLOBAL` object. You can use it as a coordinate system.

#### Change lcs and rcs
You can change lcs and rcs with `part.change_cs` method. It accepts the following arguments:
- `lcs`: CoordinateSystem, if defined, it will be the new local coordinate system of the part.
- `rcs`: CoordinateSystem, if defined, it will be the new reference coordinate system of the part. use `tdo.GLOBAL` cs to defined the global cs as the rcs.
```python
lens.change_cs(lcs = lens.cs[1])
detector.change_cs(rcs = lens.cs[0])
ls.change_cs(lcs = ls.cs[0], rcs = tdo.GLOBAL)
```

### Materials
#### Find Materials From Database
Some mmethods require specific materials from our database. In order to find them, use `client.search_materials` method.
```python
materials = client.search_materials('N-BK7')
```
`materials` is now a list of `tdo.Material` object.
```python
for m in materials:
    m.describe()
```
Finally, you can use the chosen material object or its material id directly.

### Analysis
`tdo.Analysis` are the objects that represent analyses that can be performed on a surface.
They are defined by:

- `id`: The unique id of the analysis.
- `surface`: The `tdo.Surface` object on which the analysis will be made.
- `resolution`: The analysis surface resolution, in the format of `[pixels_x, pixels_y]` (up to 1e4)
- `rays`: A dictionary that maps how many rays to shoot from each light source (up to 1e9), in the format of `{ls_object: num_rays, ls_object: num_rays, ...}` where light source object is a `tdo.LightSource` object. The rays are distributed equally between the light source wavelengths.
- `name`: str, one of `tdo.ANALYSIS_NAMES`.

A surface can contain several analysis with identical properties and different ids.
However, each analysis consumes your account resources, since analysis id holds its results.
When you run the analysis again, the last result is deleted from 3DOptix systems.
So, we reccomend storing iterations of the same analysis locally and use duplicated analyses only when you think it's necessary.

#### Find existing analysis

Every new analysis consumes storage resources for your account.
So, we reccomend sticking to the same analysis if they have the same properties instead of creating new ones.
You could get a list of the `tdo.Analysis` of the surface like this:

```python
setup = client.get('example')
detector = setup.get('my_detector')
detector_front = detector.get('front')
detector_front_analyses = detector_front.analyses

# Then, you could check their properties and choose the right one:

for analysis in detector_front_analyses:
    print(analysis)
```

Or get an existing analyses with required parameters, if the id doesn't matter:

```python
detector_front = setup.get('my_detector').get('front')
analysis = detector_front.find_analysis(name = name, rays = rays, resolution = resolution)
```

#### Create and add analysis

If you want to create an analysis that doesn't exist for the surface yet, or you want to create a duplicated analysis, we can create one:

```python
analysis = tdo.Analysis(surface: tdo.Surface,
                        name: str,
                        rays: dict {ls_object: int, ...}
                        resolution: list [int, int]
                        )
```

For example:

```python
laser = setup.get('ls')
surface = detector.get('front')

analysis1 = tdo.Analysis(surface = surface,
                        resolution = [100, 200],
                        rays = {laser: 1e5, laser2: 1e4},
                        name = "Spot (Incoherent Irradiance)"
                        )
analysis2 = tdo.Analysis(surface = surface,
                        resolution = 100, #for equal height and width pixels
                        rays = 1e6, #for all of the lasers in the setup
                        name = "Spot (Incoherent Irradiance)"
                        )
```

> **Reminder**
> You can always access all the possible analysis names with `tdo.ANALYSIS_NAMES`

After we created an analysis, we need to add it to the surface and setup to be able to run it.

```python
# In case the surface doesn't have analysis with this parameter
surface.add_analysis(analysis)

# In case that the surface has an analysis with these parameter, and we want to add a new one anyway
surface.add_analysis(analysis, force = True)
```

**If the analysis is duplicated**, you have to use `force = True` to indicate that you understand that you are adding a duplicated analysis that will use more storage.
Otherwise, you will get an error.
#### Delete Analysis
You can delete analysis from the surface with `surface.delete_analysis(analysis)` method.
This can help manage memory as well as creating more smooth workflows.
```python
results = setup.run(analysis)
analysis.show()
surface.delete_analysis(analysis)
```

## Make Changes

#### Transformations

You could move and rotate part using `part.change_pose()` method that moves the part to a location on the three axis (x, y, z) and rotates it in respect to them (alpha, beta, gamma).

All six numbers indicating absolute future value in respect to the part's coordinate system, **not** change and **not** with respect to the global coordinate system.
if you want to change coordinate systems, please check `part.change_cs` method.

```python
#Define the rotation
new_pose = [x, y, z, alpha, beta, gamma]

#Apply on the part
part.change_pose(new_pose)

# In case that the rotation is in radians
part.change_pose(new_pose, radians = True)

#Verify change
assert part.pose == new_pose
```

At the beginning, we reccomend frequent sanity-checks in the GUI to make sure you got everything right.

> **Note**
> Rotation is stated using **degrees** by default.
> use `part.change_pose(new_pose, radians = True)` for radians.

> **Reminder**
> Changing the pose of a part also changes the poses of every part that is related to its coordinate system.

#### Change part's label

It's possible to change part's label:

```python
part.change_label(new_label)
```

At the beginning, we reccomend frequent sanity-checks in the GUI to make sure you got everything right.

#### Modify Detectors

Detectors have a `detector.change_opacity()` and `detector.change_size()` methods, that changes the detector's opacity and size, accordingly.
This is how you use them:

```python
# Get the detector
detector = setup.get('detector_label')

#Apply changes
detector.change_size([new_half_height, new_half_width])
detector.change_opacity(new_opacity)
detector.change_pose([x, y, z, alpha, beta, gamma])

#Verify change
print(detector.size, detector.opacity, detector.pose)
```

At the beginning, we reccomend frequent sanity-checks in the GUI to make sure you got everything right.

### Modify Light Sources

#### Change wavelengths

Light sources have a `light_source.change_wavelengths()` and `light_source.add_wavelengths()` methods, that changes the light source's wavelengths or add new ones, accordingly.
**In both cases**, you could pass a `list` of equal weight wavelengths or a `dict`, defining wavelength-weight pairs.
This is how you use them:

```python
# Get the light source
light_source = setup['light_source_id']

#Backup the original light source's state
light_source.backup()

#For equal-weight wavelengths
new_wavelengths = [550, 600, 650]
#For non-equal weight wavelengths
new_wavelengths = {550: 0.5, 600: 0.7, 700: 0.3}

#Change the wavelengths completely
light_source.change_wavelengths(new_wavelengths)
#Add new ones
light_source.add_wavelengths(new_wavelengths)

#Change pose
light_source.change_pose([x, y, z, alpha, beta, gamma])

#Verify change
print(light_source.wavelengths, light_source.pose)
```

At the beginning, we reccomend frequent sanity-checks in the GUI to make sure you got everything right.

**Create normal distribution**
If you want to create wavelengths spectrum with a normal disribution, you could use `tdo.utils.wavelengths_normal_distribution`:

```python
# Define the spectrum
wavelengths_spectrum = tdo.wavelengths_normal_distribution(mean_wavelength, std_dev, num_wavelengths)

# Modify the light source
light_source.change_wavelengths(wavelengths_spectrum)
```
Where:

- `mean_wavelength` is the mean wavelength of the distribution
- `std_dev` is the standard deveation of the distribution
- `num_wavelengths` is the number of the wavelengths that will be sampled.

**Create uniform distribution**
Similarly, If you want to create wavelengths spectrum with a uniform disribution, you could use `tdo.utils.wavelengths_uniform_distribution`:

```python
# Define the spectrum
wavelengths_spectrum = tdo.wavelengths_uniform_distribution(min_wavelength, max_wavelength, num_wavelengths)

# Modify the light source
light_source.change_wavelengths(wavelengths_spectrum)
```

Where:

- `min_wavelength` is the minimum wavelength of the distribution
- `max_wavelength` is the maximum wavelength of the distribution
- `num_wavelengths` is the number of the wavelengths that will be sampled.

#### Change to gaussian beam

`ls.to_gaussian()` allows you to change the light source beam to a gaussian and define it.
Arguments:

- `waist_x`: float
- `waist_y`: float
- `waist_position_x`: float
- `waist_position_y`: float

For example:

```python
ls = setup['light_source_id']

gaussian_beam_config = {
    "waist_x": 1,
    "waist_y": 1,
    "waist_position_x": 0,
    "waist_position_y": 0
}

ls.to_gaussian(**gaussian_beam_config)
```

#### Change to plane wave beam

`ls.to_point_source()` allows you to change the light source beam to a point source and define it.
Arguments:

- `density_pattern`: str, one of:
  - "XY_GRID"
  - "CONCENTRIC_CIRCLES"
  - "RANDOM"
- `plane_wave_data`: dict, with the following entries:
  - "source_shape", One of:
    - "RECTANGULAR"
    - "ELLIPTICAL"
    - "CIRCULAR"
  - If type is "RECTANGULAR":
    - "width", "height": floats, the width and height of the beam
  - If type is "CIRCULAR":
    - "radius": float, the radius of the beam
  - If type is "ELLIPTICAL":
    - "radius_x", "radius_y": floats, the radii of the beam.

For example:

```python
plane_wave_data = {
    "source_shape": "RECTANGULAR",
    "width": 10,
    "height": 10
}

plane_wave_config = {
    "density_pattern": "CONCENTRIC_CIRCLES",
    "plane_wave_data": plane_wave_data
}

ls.to_plane_wave(**plane_wave_config)
```

```python

plane_wave_data = {
    "source_shape": "CIRCULAR",
    "radius": 5,
}

plane_wave_config = {
    "plane_wave_data": plane_wave_data,
    "density_pattern": "XY_GRID"
}

ls.to_plane_wave(**plane_wave_config)
```

```python
plane_wave_data = {
    "source_shape": "ELLIPTICAL",
    "radius_x": 7,
    "radius_y": 7
}
plane_wave_config = {
    "plane_wave_data": plane_wave_data,
    "density_pattern": "RANDOM"
}

ls.to_plane_wave(**plane_wave_config)

```

#### Change to point source beam

`ls.to_point_source()` allows you to change the light source beam to a point source and define it.
Arguments:

- `density_pattern`: str, one of:
  - "XY_GRID"
  - "CONCENTRIC_CIRCLES"
  - "RANDOM"
- `model_radius`: float, the model radius between 1 and 10.
- `data`: dict, with the following entries:
  - "type", One of:
    - "HALF_CONE_ANGLE"
    - "HALF_WIDTH_RECT"
    - "HALF_WIDTH_AT_Z"
  - If type is "HALF_WIDTH_AT_Z":
    - "dist_z": float, determine the distance to calculate the half_width_x_at_dist and half_width_y_at_dist
    - "half_width_x_at_dist": float, determines the half width on x-axis at dist_z.
    - "half_width_y_at_dist": float, determines the half width on y-axis at dist_z.
  - Otherwise:
    - "angle_y": float, Y-axis opening angle.
    - "angle_x": float, X-axis opening angle

For example:

```python
ls = setup.get('light_source_label')
point_source_data = {
    "type": "HALF_CONE_ANGLE",
    "angle_y": 10,
    "angle_x": 10
}
point_source_config = {
    "point_source_data": point_source_data,
    "density_pattern": "XY_GRID",
    "model_radius": 1
}
ls.to_point_source(**point_source_config)
```

```python
point_source_data = {
    "type": "HALF_WIDTH_AT_Z",
    "dist_z": 50,
    "half_width_x_at_dist": 10,
    "half_width_y_at_dist": 10,
}
point_source_config = {
    "point_source_data": point_source_data,
    "model_radius": 1,
    "density_pattern": "RANDOM"
}
ls.to_point_source(**point_source_config)
```

#### Change other properties

Other changable properties are:

- `ls.change_power(new_power: float)`: A float between 0 and 1e6.
- `ls.change_rays_direction(phi, theta, azimuth_z)`: The new rays direction parameter
- `ls.change_vis_count(new_vis_count: int)`: An int between 1 and 200, the number of visualization rays in the app.
- `ls.change_vis_count_type(count_type: str)`: "TOTAL" if `ls.vis_count` is the total number of rays. "PER_WAVELENGTH" if it's per wavelengths of the light source.
- `ls.change_opacity(new_opacity: float)`: A float between 0 and 1.
- `ls.change_color(color: str)`: A hexidecimal representation of the visualization color in the GUI.

At the beginning, we reccomend frequent sanity-checks in the GUI to make sure you got everything right.

### Modify Several Properties Together

Changing multiple parameters sequentially can be time consuming.
In order to change several properties together at one time faster, you could use `part.change_config`.
In most cases, the argument are the same arguments of the original method.
In light source source type, it's a dictionary with the arguments and values of the appropriate method.

#### Modify multiple properties of parts

```python
part = setup.get('part_label')
part.change_config(label: str,
                   pose: list[float]
                   )
```

#### Modify multiple properties of detectors

```python
detector = setup['detector_id']
detector.change_config(pose: str,
                      label: str,
                      size: tuple,
                      opacity: float
                      ):
```

#### Modify multiple properties of light sources

```python
light_source = setup['light_source_id']
light_source.change_config(pose: list, #[0, 0, 0, 0, 0, 0,]
                           label: str, #"New label"
                           wavelengths: Union[dict,list], #{550: 0.5, 650: 1}
                           add_wavelengths: Union[dict, list], #{750: 1, 850: 0.5}
                           power: float, #1
                           vis_count: int, #150
                           count_type: str, #TOTAL
                           rays_direction_config: dict, #{'theta': 0, "phi": 0, "azimuth_z": 10}
                           opacity: float, # 0.5
                           color: str, # "#000000"
                           gaussian_beam: dict, #config
                           point_source: dict, #config
                           plane_wave: dict #config
                           ):
```

`gaussian_beam`, `point_source` and `plane_wave` should be the same dictionaries defined in `to_gaussian`, `to_point_source`, and `to_plane_wave`.

> **Reminder**
> For beginners, we reccomend step-by-step changes with frequent sanity-checks in the GUI to make sure you got everything right.

## Run Simulations And Analyses

#### Simulations

Running the simulation is really simple:

```python
#run the simulation
ray_table = setup.run()

#Save the data locally
data_path = 'path/to/save/data.csv'
result.to_csv(data_path)

#View them as pd.DataFrame
results
```

The ray table is a custom `pd.DataFrame` object where each line is a single ray. The columns are:

- **Ox, Oy, Oz**: The origin point of the ray for each axis (mm).
- **Dx, Dy, Dz**: The initial direction of the ray for each axis.
- **Hx, Hy, Hz**: The hit position of the ray for each axis (mm).
- **wavelength**: The wavelength of the ray (nm).
- **Ap**: The p amplitude of the ray.
- **As**: The s amplitude of the ray.
- **phase_s**: The s phase of the ray.
- **phase_p**: The p phase of the ray.
- **refractive_index**: The refractive index of the medium that the ray pass through.
- **diffraction_order**: If the element is gratings, the order of diffraction of the ray. Else- 0.
- **f_s**: Fernel coefficient s.
- **f_p**: Fernel coefficient p.
- **surface**: The index of the surface that the ray hit, when -1 means no hit.
- **light_source**: The index of the light source that generated the ray.
- **parent_idx**: The index of the predecessor ray.
- **family_idx**: The index of the origin ray.

| idx | Ox           | Oy          | Oz          | Dx             | Dy              | Dz           | As          | Ap          | phase_s      |
| --- | ------------ | ----------- | ----------- | -------------- | --------------- | ------------ | ----------- | ----------- | ------------ |
| 105 | 7.383775711  | 102.4612579 | 150.5897217 | -0.02501097694 | -0.008337006904 | 0.9996524453 | 2126145.5   | 2133974.0   | 3.118281841  |
| 114 | -12.16847992 | 92.69891357 | 151.9878235 | 0.04484132305  | 0.02690477483   | 0.9986317754 | 2056683.875 | 2082956.125 | 5.680591106  |
| 173 | 5.660968781  | 103.3965912 | 250.0       | -0.06809257716 | -0.04085547104  | 0.9968421459 | 2481887.5   | 2514519.5   | 1.11269021   |
| 186 | -1.279565811 | 101.2795563 | 250.0000153 | 0.01233130135  | -0.01233132742  | 0.9998478889 | 2591881.75  | 2593823.0   | 1.747841358  |
| 212 | 5.587198734  | 96.64768219 | 251.0799866 | -0.06809251755 | 0.04085548222   | 0.9968422651 | 2481887.5   | 2514519.5   | 0.2006378919 |

| phase_p      | diffraction_order | Hx           | Hy          | Hz          | f_s          | f_p          | refractive_index |
| ------------ | ----------------- | ------------ | ----------- | ----------- | ------------ | ------------ | ---------------- |
| 3.118281841  | 0.0               | 7.148333549  | 102.3827744 | 160.0       | 0.7891492248 | 0.7908383608 | 1.518522382      |
| 5.680591106  | 0.0               | -11.80871105 | 92.91477966 | 160.0       | 0.7770783901 | 0.782813549  | 1.518522382      |
| 1.11269021   | 0.0               | 5.58719492   | 103.3523254 | 251.0800018 | 1.0          | 1.0          | 1.0              |
| 1.747841358  | 0.0               | -1.266245365 | 101.266243  | 251.0800018 | 1.0          | 1.0          | 1.0              |
| 0.2006378919 | 0.0               | 2.182572842  | 98.69045258 | 300.9220886 | 1.0          | 1.0          | 1.0              |

| parent_idx | family_idx | surface     | wavelength | light_source |
| ---------- | ---------- | ----------- | ---------- | ------------ |
| 89.0       | 9.0        | LP86NPVUVMR | 550        | LP86R718Q6B  |
| 66.0       | 18.0       | LP86NPVUVMR | 550        | LP86R718Q6B  |
| 141.0      | 13.0       | LP86PQO2JLV | 550        | LP86R718Q6B  |
| 154.0      | 26.0       | LP86PQO2JLV | 550        | LP86R718Q6B  |
| 164.0      | 4.0        | LP86NPVY4K9 | 550        | LP86R718Q6B  |

### Analyses

#### Run

We can run analysis that is already in `surface.analyses` straight away:

```python
surface = part['surface_id']
analysis = surface.find_analysis(name = "Spot (Coherent Irradiance) Huygens",
                                 rays = {laser: 1e6, laser2: 1e8},
                                 resolution = (400, 400)
                                 )
results = setup.run(analysis)
```

If the analyses that we want is not added yet, we need to add it and then run it.
We have two ways of doing that:

```python
surface.add_analysis(analysis)
results = setup.run(analysis)
```

> **Reminder**
> If you would try to add analysis with exactly the same parameters as one that you already have, you should use **`force = True`** argument to make sure that you are interested with duplicated analysis.
> Otherwise, choose the existing analysis and run it instead. This helps optimizing your system memory credits usage.

#### Results

Even if we didn't store it in another variable, we can view and analize the latest results in a raw form:

```python
# For jupyter notebooks or HTML
display(analysis.results)

# For scripts
print(analysis.results)
```

The result will be a pandas dataframe (`pd.DataFrame`) with all the different matrices.
The columns of the dataframe are:
    - `data`: The matrix of the results for that row's configuration.
    - `polarization`: The polarization of the data.
    - `wl`: The wavelength of the data.
    - `spot_target_kind`: Can be either 'Source', 'Group' or 'Total', indicating if the data is the result of a single source, coherent group or the total results of all the light sources.
    - `spot_target`: The id of the light source\coherent group.

For example, let's say I am looking for the _"X"_ polarization, _400 nm_ rays hit matrix:

```python
mask = (results.wl == 400) & (results.polarization == 'X')
matrices = results[mask].data
```
and, ofcourse, any `pd.DataFrame` manipulation will work as usuall.

> **Note**
> If you plan on running the anlysis again, it is really important to store a deepcopy of analysis.results in the `matrix` variable.
> Otherwise, the variable will hold the pointer to the `results` property of the analysis, and the previous results will be overriden.
> Another option is to store the results of `setup.run(analysis)` in another variable, since it outputs a copy anyway.

If we want to see the matrices as a images, we can simply:

```python
#for static figure
tdo.show_matrix(matrix)

#for interactive figure
tdo.show_matrix(matrix, interactive = True)
```

## Create a new `tdo.Optics` in your product catalog
As for now, the SDK supports creating spherical and conic lenses.
### Create Lenses
#### Spherical Lenses
To create spherical lens, we can use `client.create_spherical_lens` method. The arguments are:
- `name`: str, the name of the created lens.
- `material`: Union[str, tdo.Material], the desired material id or material object of the lens. Can be found using `client.search_materials(material_name)` method.
- `diameter`: float, the diameter of the lens.
- `thickness`: float, the central thickness of the lens.
- `r1`: float, the first radius of curvature.
- `r2`: float, the second radius of curvature.

The method returns the number id of the created element.
```python
lens_db_id = client.create_spherical_lens(name = name,
                                              material = material,
                                              diameter = diameter,
                                              thickness = thickness,
                                              r1 = r1,
                                              r2 = r2)
```

#### Conic Lenses
To create conic lens, we can use `client.create_conic_lens` method. The arguments are:
- `name`: str, the name of the created lens.
- `material`: Union[str, tdo.Material], the desired material id or material object of the lens. Can be found using `client.search_materials(material_name)` method.
- `diameter`: float, the diameter of the lens.
- `thickness`: float, the central thickness of the lens.
- `r1`: float, the first radius of curvature.
- `r2`: float, the second radius of curvature.
- `k1`, `k2`: float, the conic coefficients of the lens. Default to 0.

The method returns the number id of the created element.
```python
lens_db_id = client.create_spherical_lens(name = name,
                                              material = material,
                                              diameter = diameter,
                                              thickness = thickness,
                                              r1 = r1,
                                              r2 = r2,
                                              k1 = k1,
                                              k2 = k2)
```

#### Biconic Lenses
To create conic lens, we can use `client.create_conic_lens` method. The arguments are:
- `name`: str, the name of the created lens.
- `material`: Union[str, tdo.Material], the desired material id or material object of the lens. Can be found using `client.search_materials(material_name)` method.
- `diameter`: float, the diameter of the lens.
- `thickness`: float, the central thickness of the lens.
- `r1_x`, `r1_y`: float, the first radius of curvature.
- `r2_x`, `r2_y`: float, the second radius of curvature.
- `k1_x`, `k1_y`, `k2_x`, `k2_y`: float, the conic coefficients of the lens. Default to 0.

The method returns the number id of the created element.
```python
lens_db_id = client.create_spherical_lens(name = name,
                                          material = material,
                                          diameter = diameter,
                                          thickness = thickness,
                                          r1_x = r1_x,
                                          r1_y = r1_y,
                                          r2_x = r2_x,
                                          r2_y = r2_y,
                                          k1_x = k1_x,
                                          k1_y = k1_y,
                                          k2_x = k2_x,
                                          k2_y = k2_y)
```
### Create Grating
You can create a new grating in the database with `client.create_grating` method.
It requires the following arguments:
- `name`: str, The name of the grating in the database.
- `material`: Union[str, tdo.Material], the desired material id or material object of the lens. Can be found using `client.search_materials(material_name)` method.
- `grooves`: int, Number of grooves on the grating.
- `order`: int, order of diffraction.
- `orientation_vector`: iter, a 3 floats iterable representing the normalized orientation vector of the grooves.
- `gating_side`: `"Front"` or `"Back"`, the surface of the grating element onto which the grating structure would apply. Default to `"Front"`
- `thickness`: float, the thickness of the grating.
- `shape`: 'cir' or 'rec', representing circular or rectangular grating.
    - if `shape` is `"cir"`, then `diameter` must to be specified.
    - if `shape` is `"rec"`, then `height`, `width` must to be specified.
- `subtype`: str, one of `tdo.GRATING_SUBTYPES`.
    - if `subtype` is one of `"Blazed Ruled Reflective Grating"`, `"Echelle Grating"`, `"Transmission Grating"`: `blaze_angle` and `blaze_wavelength` must also be specified.

For example:
```python
circular_grating_id = client.create_grating(name = 'example circular grating',
                                            material = material,
                                            orientation_vector = [1, 0, 0],
                                            shape = 'cir',
                                            thickness = 3,
                                            diameter = 5,
                                            subtype = 'Reflective Grating',
                                            grooves = 200,
                                            order = 2,
                                            )
```
```python
rectangular_transmission_grating_id = client.create_grating(name = 'example circular grating',
                                                            material = material2,
                                                            orientation_vector = [0, 1, 0],
                                                            shape = 'rec',
                                                            thickness = 3,
                                                            height = 2,
                                                            width = 1.5,
                                                            subtype = 'Transmission Grating',
                                                            grooves = 200,
                                                            order = 2,
                                                            blaze_angle = 20,
                                                            blaze_wavelength = 450
                                                            )
```

## Advanced
### Utils Module
#### Get spot size

`tdo.utils.calculate_spot_size(matrix)` calculates the diameter of the blocking circle of the biggest contours of the matrix, in pixels.

```python

# Assuming that this analysis exists already
setup = client['setup_id']
detector = setup.get('detector_label')
detector_front = detector.get('front')

analysis = detector_front.analysis_with(name ="Spot (Incoherent Irradiance)",
                                        rays = {laser1: 2.5e6, laser2: 2.5e6},
                                        resolution = (1000, 1000)
                                        )
# Run the analysis
results = setup.run(analysis)

# Calculate spot size
spot_size_dia = tdo.calculate_spot_size(results.data[0])
print(f'Analysis spot size diameter for X polarization at 550 nm is {spot_size_dia}')
```

`tdo.utils.encircled_energy(matrix, percent)` calculates the diameter of the circle that centers at the center of energy mass, and contains `percantage` of the matrix's total energy.

```python
encircled_energy_radius, center = tdo.encircled_energy(matrix, 0.9)
print(f'Analysis encircled 90% energy radius for X polarization at 550 nm is {encircled_energy_radius} with the center at {center}')
```

Of course, these values are pixel values. In order to get absolute values in length units, use `tdo.utils.absolute_pixel_size`:

```python
pixel_radius, center = tdo.encircled_energy(matrix, 0.95)
absolute_radius = tdo.absolute_pixel_size(detector.size, analysis.resolution)[0] * pixel_radius # Assuming that the resolution is symmetrical
print(f'95% Encircled energy radius is {absolute_radius} mm')
```

#### Scans

In order to perform a scan, all we need to do is to define an analysis:

```python
analysis = tdo.Analysis(name = "Spot (Incoherent Irradiance)",
                        rays = {light_source: 1e5, light_source2: 5e4}
                        resolution = [500, 500],
                        surface = detector.get('front')
                        )
detector_front.add_analysis(analysis)
```

Or choosing an existing one:

```python
analysis = detector_front.analysis_with(name = name,
                                        rays = rays,
                                        resolution = resolution
                                        )
assert analysis is not None
```

Then, we need to iteratively change the properties of some part in the setup and store the results.

```python
def scan_z(lens, analysis, dz_range, steps):

    # Store the original pose
    original_pose = lens.pose.copy()

    # Store the results here
    results_history = []

    # Iterate over the lens location in the z axis
    for dz in np.arange(dz_range[0], dz_range[1] + steps, steps):

        #Define absolute new pose
        delta = [0, 0, dz, 0, 0, 0]
        new_pose = [j+h for j, h in zip(original_pose, delta)]

        # Apply changes
        lens.change_pose(new_pose)

        # Run analysis
        results = setup.run(analysis)
        results = {"dz": dz, "results": results}

        # Store them
        results_history.append(results)

    return results_history

results = scan_z(lens, analysis, (-1, 1), 0.1)
```

Similarly, you will be able to perform grid scan, changing multiple parameters together.

#### Optimizations

If you have a merit or loss function you wish to optimize or minimize, consider using `tdo.optimize`.
Here are few examples:

```python
import threed_optix.optimize as opt

def loss(new_yz):

    # Define absolute new pose
    y, z = new_yz
    new_pose = original_pose.copy()
    new_pose[1] = y
    new_pose[2] = z

    # Change len's pose
    lens.change_pose(new_pose)

    # Run analysis
    results = setup.run(analysis)

    # Get the right image
    image = results.data[1] # Assuming that the second line is the matrix of interst

    # Calculate spot size can be any function that returns a scalar you want to minimize.
    spot_size_diameter = tdo.calculate_spot_size(image)

    print(f"dz: {dz}, dy: {dy}, spot size: {spot_size_diameter}")
    return spot_size_diameter

# Assuming the initial guess is the current lens position
lens = setup.get('lens1')
original_pose = lens.pose.copy()

y = original_pose[1]
z = original_pose[2]
initial_guess = [y, z]

# Define bounds to avoid getting out of desired range
low_y = y -1
high_y = y + 1
low_z = z -1
high_z = z + 1
bounds = [(low_y, high_y), (low_z, high_z)]

# Execute search
result = opt.minimize(loss, initial_guess, method='Nelder-Mead', bounds = bounds)

# Get the optimized values
best_y, best_z = result.x

# Output the best values found
print(f"Best z: {best_z}, Best y: {best_y}")

best_pose = original_pose.copy()
best_pose[1] = best_y
best_pose[2] = best_z
lens.change_pose(best_pose)
```

Ofcourse, the optimization will be done up to the point where there is no change in the pixel radius.
In order to bypass this, you could make the detector smaller and smaller as the iteration goes.
If you do so, you should return the absolute value, rather then pixel one.

#### Matlab code

If you have a **general** matlab code you wish to use in our SDK, you could simply translate it to python. We recommend using `matlab2python` library from the github repo:

```bash
pip install matlab2python@git+https://github.com/ebranlard/matlab2python.git#egg=m
atlab2python
```

And then use in your code:

```python
import matlabparser as mpars

mlines="""# a comment
x = linspace(0,1,100);
y = cos(x) + x**2;
"""
pylines = mpars.matlablines2python(mlines, output='stdout')
print(pylines)
```

> **Warning**
> This is an external library that's not part of our SDK, nor was built by us.
> Use output code with caution.

# License

3DOptix API is available with [MIT License](https://choosealicense.com/licenses/mit/).
