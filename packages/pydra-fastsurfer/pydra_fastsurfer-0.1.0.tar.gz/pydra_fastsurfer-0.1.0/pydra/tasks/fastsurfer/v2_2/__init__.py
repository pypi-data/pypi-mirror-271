from pydra.engine import specs
from pydra.engine import ShellCommandTask
import typing as ty
from pathlib import Path
from fileformats.generic import File, Directory
from fileformats.medimage import MghGz


input_fields = [
    (
        "subjects_dir",
        Path,
        {
            "help_string": "Subjects directory",
            "argstr": "--sd {subjects_dir}",
            "output_file_template": "subjects_dir",
        },
    ),
    (
        "subject_id",
        ty.Any,
        {
            "help_string": "Subject ID",
            "argstr": "--sid {subject_id}",
            "mandatory": True,
        },
    ),
    (
        "T1_files",
        File,
        {
            "help_string": "T1 full head input (not bias corrected, global path)",
            "argstr": "--t1 {T1_files}",
            "mandatory": False,
        },
    ),
    (
        "fs_license",
        File,
        {
            "help_string": "Path to FreeSurfer license key file.",
            "argstr": "--fs_license {fs_license}",
        },
    ),
    (
        "seg",
        File,
        {"help_string": "Pre-computed segmentation file", "argstr": "--seg {seg}"},
    ),
    (
        "weights_sag",
        File,
        {
            "help_string": "Pretrained weights of sagittal network",
            "argstr": "--weights_sag {weights_sag}",
            "mandatory": False,
        },
    ),
    (
        "weights_ax",
        File,
        {
            "help_string": "Pretrained weights of axial network",
            "argstr": "--weights_ax {weights_ax}",
            "mandatory": False,
        },
    ),
    (
        "weights_cor",
        File,
        {
            "help_string": "Pretrained weights of coronal network",
            "argstr": "--weights_cor {weights_cor}",
            "mandatory": False,
        },
    ),
    (
        "seg_log",
        File,
        {
            "help_string": "Name and location for the log-file for the segmentation (FastSurferCNN).",
            "argstr": "--seg_log {seg_log}",
            "mandatory": False,
        },
    ),
    (
        "clean_seg",
        bool,
        {
            "help_string": "Flag to clean up FastSurferCNN segmentation",
            "argstr": "--clean_seg",
            "mandatory": False,
        },
    ),
    (
        "run_viewagg_on",
        File,
        {
            "help_string": "Define where the view aggregation should be run on.",
            "argstr": "--run_viewagg_on {run_viewagg_on}",
            "mandatory": False,
        },
    ),
    (
        "no_cuda",
        bool,
        {
            "help_string": "Flag to disable CUDA usage in FastSurferCNN (no GPU usage, inference on CPU)",
            "argstr": "--no_cuda",
            "mandatory": False,
        },
    ),
    (
        "batch",
        int,
        16,
        {
            "help_string": "Batch size for inference. default=16. Lower this to reduce memory requirement",
            "argstr": "--batch {batch}",
            "mandatory": False,
        },
    ),
    (
        "fstess",
        bool,
        {
            "help_string": "Use mri_tesselate instead of marching cube (default) for surface creation",
            "argstr": "--fstess",
            "mandatory": False,
        },
    ),
    (
        "fsqsphere",
        bool,
        {
            "help_string": "Use FreeSurfer default instead of novel spectral spherical projection for qsphere",
            "argstr": "--fsqsphere",
            "mandatory": False,
        },
    ),
    (
        "fsaparc",
        bool,
        {
            "help_string": "Use FS aparc segmentations in addition to DL prediction",
            "argstr": "--fsaparc",
            "mandatory": False,
        },
    ),
    (
        "no_surfreg",
        bool,
        {
            "help_string": "Skip creating Surface-Atlas (sphere.reg) registration with FreeSurfer\n        (for cross-subject correspondence or other mappings)",
            "argstr": "--no_surfreg",
            "mandatory": False,
        },
    ),
    (
        "parallel",
        bool,
        True,
        {
            "help_string": "Run both hemispheres in parallel",
            "argstr": "--parallel",
            "mandatory": False,
        },
    ),
    (
        "threads",
        int,
        4,
        {
            "help_string": "Set openMP and ITK threads to",
            "argstr": "--threads {threads}",
            "mandatory": False,
        },
    ),
    (
        "py",
        ty.Any,
        "python3.8",
        {
            "help_string": "which python version to use. default=python3.6",
            "argstr": "--py {py}",
            "mandatory": False,
        },
    ),
    (
        "seg_only",
        bool,
        {
            "help_string": "only run FastSurferCNN (generate segmentation, do not surface)",
            "argstr": "--seg_only",
            "mandatory": False,
        },
    ),
    (
        "surf_only",
        bool,
        {
            "help_string": "only run the surface pipeline recon_surf.",
            "argstr": "--surf_only",
            "mandatory": False,
        },
    ),
]
fastsurfer_input_spec = specs.SpecInfo(
    name="Input", fields=input_fields, bases=(specs.ShellSpec,)
)


def subject_dir_path(subjects_dir: Path):
    return Path(subjects_dir) / "FS_outputs"


def norm_img_path(subjects_dir: Path):
    return Path(subjects_dir) / "FS_outputs" / "mri" / "norm.mgz"


# # Update this section when Docker is being used
def aparcaseg_img_path(subjects_dir: Path):
    return Path(subjects_dir) / "FS_outputs" / "mri" / "aparc+aseg.mgz"


def brainmask_img_path(subjects_dir: Path):
    return Path(subjects_dir) / "FS_outputs" / "mri" / "brainmask.mgz"


output_fields = [
    (
        "subjects_dir",
        Directory,
        {
            "help_string": "Subjects directory",
            "argstr": "--sd {subjects_dir}",
            "output_file_template": "subjects_dir",
        },
    ),
    (
        "subjects_dir_output",
        Directory,
        {
            "help_string": "path to subject FS outputs",
            "callable": subject_dir_path,
        },
    ),
    (
        "norm_img",
        MghGz,
        {
            "help_string": "norm image",
            "callable": norm_img_path,
        },
    ),
    (
        "aparcaseg_img",
        MghGz,
        {
            "help_string": "aparc+aseg image",
            "callable": aparcaseg_img_path,
        },
    ),
    (
        "brainmask_img",
        MghGz,
        {
            "help_string": "brainmask.mgz image",
            "callable": brainmask_img_path,
        },
    ),
]
fastsurfer_output_spec = specs.SpecInfo(
    name="Output", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Fastsurfer(ShellCommandTask):
    """
    Examples
    -------

    >>> from fileformats.generic import File
    >>> from pydra.tasks.fastsurfer.v1.fast_surfer import fast_surfer

    """

    input_spec = fastsurfer_input_spec
    output_spec = fastsurfer_output_spec
    executable = "run_fastsurfer.sh"
