import os
from surfquakecore.moment_tensor.mti_parse import read_isola_result, WriteMTI
from surfquakecore.moment_tensor.sq_isola_tools.sq_bayesian_isola import BayesianIsolaCore
from surfquakecore.project.surf_project import SurfProject


if __name__ == "__main__":
    cwd = os.path.dirname(__file__)

    inventory_path = "/Users/roberto/Desktop/all_andorra/metadata/inv_all.xml"

    path_to_project = "/Users/roberto/Desktop/all_andorra/project/surfquake_project_year.pkl"
    path_to_configfiles = "/Users/roberto/Desktop/all_andorra/mti_configs"
    output_directory = "/Users/roberto/Desktop/all_andorra/mti"

    # Load the Project
    sp = SurfProject.load_project(path_to_project_file=path_to_project)
    print(sp)

    # Build the class
    bic = BayesianIsolaCore(project=sp, inventory_file=inventory_path, output_directory=output_directory,
                            save_plots=True)

    # Run Inversion
    bic.run_inversion(mti_config=path_to_configfiles)
    print("Finished Inversion")
    wm = WriteMTI(output_directory)
    file_output = os.path.join(output_directory, "mti_summary.txt")
    wm.mti_summary(file_output)
