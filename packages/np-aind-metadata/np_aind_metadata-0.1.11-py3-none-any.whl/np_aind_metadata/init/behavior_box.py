# import datetime
# import logging
# import typing

# from aind_data_schema.core import rig
# from aind_data_schema.models import coordinates, devices, organizations

# from np_aind_metadata import common


# DEFAULT_HOSTNAME = "127.0.0.1"


# logger = logging.getLogger(__name__)


# def get_rig_room(rig_name: common.RigName) -> typing.Union[str, None]:
#     rig_to_room = {
#         "NP0": "325",
#         "NP1": "325",
#         "NP2": "327",
#         "NP3": "342",
#     }
#     try:
#         return rig_to_room[rig_name]
#     except KeyError:
#         logger.debug("No room found for rig: %s" % rig_name)
#         return None


# def init(
#     rig_name: common.RigName,
#     modification_date: typing.Optional[datetime.date] = None,
#     mon_computer_name: str = DEFAULT_HOSTNAME,
#     stim_computer_name: str = DEFAULT_HOSTNAME,
#     sync_computer_name: str = DEFAULT_HOSTNAME,
# ) -> rig.Rig:
#     """Initializes a rig model for the dynamic routing project.

#     >>> rig_model = init("NP3")

#     Notes
#     -----
#     - rig_id is expected to be in the format:
#         <ROOM NAME>_<RIG NAME>_<MODIFICATION DATE>
#     - The DR task does not set the brightness and contrast of the monitor.
#      These are hardcoded and assumed to be static.
#     """
#     if not modification_date:
#         modification_date = datetime.date.today()

#     room_name = get_rig_room(rig_name)
#     rig_id = f"{rig_name}_{modification_date.strftime('%y%m%d')}"
#     if room_name is not None:
#         rig_id = f"{room_name}_{rig_id}"

#     model = rig.Rig(
#         rig_id=rig_id,
#         modification_date=modification_date,
#         modalities=[
#             rig.Modality.BEHAVIOR_VIDEOS,
#             rig.Modality.BEHAVIOR,
#             rig.Modality.ECEPHYS,
#         ],
#         mouse_platform=devices.Disc(
#             name="Mouse Platform",
#             radius="4.69",
#             radius_unit="centimeter",
#             notes=(
#                 "Radius is the distance from the center of the wheel to the " "mouse."
#             ),
#         ),
#         stimulus_devices=[
#             devices.Monitor(
#                 name="Stim",
#                 model="PA248",
#                 manufacturer=organizations.Organization.ASUS,
#                 width=1920,
#                 height=1200,
#                 size_unit="pixel",
#                 viewing_distance=15.3,
#                 viewing_distance_unit="centimeter",
#                 refresh_rate=60,
#                 brightness=43,
#                 contrast=50,
#             ),
#             devices.Speaker(
#                 name="Speaker",
#                 manufacturer=organizations.Organization.ISL,
#                 model="SPK-I-81345",
#             ),
#             devices.RewardDelivery(
#                 reward_spouts=[
#                     devices.RewardSpout(
#                         name="Reward Spout",
#                         manufacturer=organizations.Organization.HAMILTON,
#                         model="8649-01 Custom",
#                         spout_diameter=0.672,
#                         spout_diameter_unit="millimeter",
#                         side=devices.SpoutSide.CENTER,
#                         solenoid_valve=devices.Device(
#                             name="Solenoid Valve",
#                             device_type="Solenoid Valve",
#                             manufacturer=organizations.Organization.NRESEARCH,
#                             model="161K011",
#                             notes="Model number is product number.",
#                         ),
#                         lick_sensor=devices.Device(
#                             name="Lick Sensor",
#                             device_type="Lick Sensor",
#                             manufacturer=organizations.Organization.OTHER,
#                         ),
#                         lick_sensor_type=devices.LickSensorType.PIEZOELECTIC,
#                         notes=(
#                             "Spout diameter is for inner diameter. "
#                             "Outer diameter is 1.575mm. "
#                         ),
#                     ),
#                 ]
#             ),
#         ],
#         ephys_assemblies=[],
#         light_sources=[],
#         cameras=[],
#         daqs=[
#             devices.DAQDevice(
#                 manufacturer=organizations.Organization.NATIONAL_INSTRUMENTS,
#                 name="Sync",
#                 computer_name=sync_computer_name,
#                 model="NI-6612",
#                 data_interface=devices.DataInterface.PCIE,
#             ),
#             devices.DAQDevice(
#                 manufacturer=organizations.Organization.NATIONAL_INSTRUMENTS,
#                 name="Behavior",
#                 computer_name=stim_computer_name,
#                 model="NI-6323",
#                 data_interface=devices.DataInterface.USB,
#             ),
#             devices.DAQDevice(
#                 manufacturer=organizations.Organization.NATIONAL_INSTRUMENTS,
#                 name="BehaviorSync",
#                 computer_name=stim_computer_name,
#                 model="NI-6001",
#                 data_interface=devices.DataInterface.PCIE,
#             ),
#             devices.DAQDevice(
#                 manufacturer=organizations.Organization.NATIONAL_INSTRUMENTS,
#                 name="Opto",
#                 computer_name=stim_computer_name,
#                 model="NI-9264",
#                 data_interface=devices.DataInterface.ETH,
#             ),
#         ],
#         detectors=[
#             devices.Detector(
#                 name="vsync photodiode",
#                 model="PDA25K",
#                 manufacturer=organizations.Organization.THORLABS,
#                 data_interface=devices.DataInterface.OTHER,
#                 notes="Data interface is unknown.",
#                 detector_type=devices.DetectorType.OTHER,
#                 cooling=devices.Cooling.AIR,
#             ),
#         ],
#         calibrations=[],
#         additional_devices=[
#             devices.Detector(
#                 name="microphone",
#                 manufacturer=organizations.Organization.DODOTRONIC,
#                 model="MOM",
#                 data_interface=devices.DataInterface.OTHER,
#                 notes="Data interface is unknown.",
#                 detector_type=devices.DetectorType.OTHER,
#                 cooling=devices.Cooling.AIR,
#             ),
#             devices.AdditionalImagingDevice(
#                 name="Galvo x",
#                 imaging_device_type=devices.ImagingDeviceType.GALVO,
#             ),
#             devices.AdditionalImagingDevice(
#                 name="Galvo y",
#                 imaging_device_type=devices.ImagingDeviceType.GALVO,
#             ),
#         ],
#         rig_axes=[
#             coordinates.Axis(
#                 name=coordinates.AxisName.X,
#                 direction=(
#                     "The world horizontal. Lays on the Mouse Sagittal Plane. "
#                     "Positive direction is towards the nose of the mouse. "
#                 ),
#             ),
#             coordinates.Axis(
#                 name=coordinates.AxisName.Y,
#                 direction=(
#                     "Perpendicular to Y. Positive direction is "
#                     "away from the nose of the mouse. "
#                 ),
#             ),
#             coordinates.Axis(
#                 name=coordinates.AxisName.Z,
#                 direction="Positive pointing up.",
#             ),
#         ],
#         origin=coordinates.Origin.BREGMA,
#         patch_cords=[
#             devices.Patch(
#                 name="Patch Cord #1",
#                 manufacturer=organizations.Organization.THORLABS,
#                 model="SM450 Custom Length, FC/PC Ends",
#                 core_diameter=125.0,
#                 numerical_aperture=0.10,
#                 notes=("Numerical aperture is approximately between 0.10 and " "0.14."),
#             ),
#         ],
#     )

#     return rig.Rig.model_validate(model)


# if __name__ == "__main__":
#     from np_aind_metadata import testmod

#     testmod()
