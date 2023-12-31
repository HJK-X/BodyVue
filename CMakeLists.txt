cmake_minimum_required(VERSION 3.10)  # 3.8 gives us built-in CUDA support; 3.10 gives us OpenGL::EGL
set(CMAKE_CXX_COMPILER g++)
set(CUDA_TOOLKIT_ROOT_DIR "/usr/local/cuda-10.0")
set(CMAKE_CUDA_COMPILER "/usr/local/cuda-10.0/bin/nvcc")
#sudo ln -s /usr/local/cuda-10.0 /usr/local/cuda
# export PATH="/usr/local/cuda-10.0/bin:/opt/cmake-3.10.3-Linux-x86_64/bin:/mnt/c/Program Files (x86)/Microsoft Visual Studio/2017/BuildTools/VC/Tools/MSVC/14.16.27023/bin/Hostx64/x64:home/bodyvue/.local/bin:/home/bodyvue/miniconda3/envs/v2a/envs/octopus/bin:/home/bodyvue/miniconda3/envs/v2a/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib:/mnt/c/Program Files/WindowsApps/MicrosoftCorporationII.WindowsSubsystemForLinux_2.0.9.0_x64__8wekyb3d8bbwe:/mnt/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.3/bin:/mnt/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.3/libnvvp:/mnt/c/Windows/system32:/mnt/c/Windows:/mnt/c/Windows/System32/Wbem:/mnt/c/Windows/System32/WindowsPowerShell/v1.0:/mnt/c/Windows/System32/OpenSSH:/mnt/c/Program Files (x86)/NVIDIA Corporation/PhysX/Common:/mnt/c/Program Files/NVIDIA Corporation/NVIDIA NvDLISR:/mnt/c/Program Files/dotnet:/mnt/c/Program Files/Docker/Docker/resources/bin:/mnt/c/Program Files/Git/cmd:/mnt/c/Program Files/NVIDIA Corporation/Nsight Compute 2023.3.1:/mnt/c/Program Files/CMake/bin:/mnt/c/Users/fdenn/miniconda3/pkgs/m2w64-binutils-2.25.1-5/Library/mingw-w64/x86_64-w64-mingw32/bin:/mnt/c/Program Files/Microsoft SQL Server/130/Tools/Binn:/mnt/c/Users/fdenn/miniconda3:/mnt/c/Users/fdenn/miniconda3/Library/mingw-w64/bin:/mnt/c/Users/fdenn/miniconda3/Library/usr/bin:/mnt/c/Users/fdenn/miniconda3/Library/bin:/mnt/c/Users/fdenn/miniconda3/Scripts:/mnt/c/Users/fdenn/AppData/Local/Microsoft/WindowsApps:/mnt/c/Users/fdenn/AppData/Local/Programs/Microsoft VS Code/bin:/mnt/c/Users/fdenn/.dotnet/tools:/mnt/c/Users/fdenn/COLMAP-3.8-windows-cuda:/mnt/c/Users/fdenn/Downloads/cudnn-10.0-windows10-x64-v7.3.0.29/cuda/bin:/snap/bin"
# export LD_LIBRARY_PATH="/usr/local/cuda-10.0/lib64/"
# export CUDA_HOME="/usr/local/cuda-10.0"
project(dirt LANGUAGES CXX CUDA) 

find_package(OpenGL REQUIRED COMPONENTS OpenGL EGL)

# Search for EGL; nvidia drivers ship the library but not headers, so we redistribute those
find_path(EGL_INCLUDE_DIR NAMES EGL/egl.h PATHS ${CMAKE_CURRENT_SOURCE_DIR}/../external REQUIRED)
find_library(EGL_LIBRARIES NAMES egl EGL REQUIRED)

# Search for cuda headers (using the form of path that tensorflow includes them with), based on cmake-inferred nvcc, or $CUDA_HOME
get_filename_component(NVCC_DIR ${CMAKE_CUDA_COMPILER} DIRECTORY)
find_path(CUDA_INCLUDE_DIR NAMES cuda/include/cuda.h HINTS ${NVCC_DIR}/../.. PATHS ENV CUDA_HOME REQUIRED)

# Manually set the path to the TensorFlow installation directory
set(TENSORFLOW_INSTALL_PATH "/home/bodyvue/miniconda3/envs/v2a/envs/octopus/lib/python3.7/site-packages/tensorflow_core")
set(TensorFlow_ROOT "/home/bodyvue/miniconda3/envs/v2a/envs/octopus/lib/python3.7/site-packages/tensorflow_core")
# Add the TensorFlow installation path to CMAKE_PREFIX_PATH
#include_directories(${TENSORFLOW_INSTALL_PATH}/include)

# Then, attempt to find TensorFlow

include_directories("/home/bodyvue/miniconda3/envs/v2a/envs/octopus/lib/python3.7/site-packages/tensorflow_core/include")


# Ask tensorflow for its compile flags; one should therefore make sure cmake is run with the venv active that the op will be used in
execute_process(COMMAND python -c "import tensorflow; print(' '.join(tensorflow.sysconfig.get_compile_flags()))" OUTPUT_VARIABLE Tensorflow_DEFAULT_COMPILE_FLAGS OUTPUT_STRIP_TRAILING_WHITESPACE)
separate_arguments(Tensorflow_DEFAULT_COMPILE_FLAGS UNIX_COMMAND "${Tensorflow_DEFAULT_COMPILE_FLAGS}")
set(Tensorflow_COMPILE_FLAGS "${Tensorflow_DEFAULT_COMPILE_FLAGS}" CACHE PATH "Tensorflow compile flags")

# Ask tensorflow for its include path; check if cuda_launch_config exists where it should
execute_process(COMMAND python -c "import tensorflow; print(tensorflow.sysconfig.get_include())" OUTPUT_VARIABLE Tensorflow_include_dir OUTPUT_STRIP_TRAILING_WHITESPACE)
if(NOT EXISTS "${Tensorflow_include_dir}/tensorflow/core/util/cuda_launch_config.h")
  if(EXISTS "${Tensorflow_include_dir}/tensorflow/core/util/gpu_launch_config.h")
    add_definitions(-DUSE_GPU_LAUNCH_CONFIG_H)
  else()
    message(FATAL_ERROR "cannot find either cuda_launch_config.h or gpu_launch_config.h")
  endif()
endif()

# Ask tensorflow for the necessary linker flags
execute_process(COMMAND python -c "import tensorflow; print(' '.join(tensorflow.sysconfig.get_link_flags()))" OUTPUT_VARIABLE Tensorflow_DEFAULT_LINK_FLAGS OUTPUT_STRIP_TRAILING_WHITESPACE)
set(Tensorflow_LINK_FLAGS "${Tensorflow_DEFAULT_LINK_FLAGS}" CACHE STRING "Tensorflow linker flags for custom ops")

# in the following, we need ../external/tensorflow for cuda_config.h in tf versions with #16959 unfixed
include_directories(SYSTEM ../external/tensorflow ${NSYNC_INCLUDE_DIR} ${CUDA_INCLUDE_DIR} ${EGL_INCLUDE_DIR} ${OPENGL_INCLUDE_DIR})
include_directories(${Tensorflow_INCLUDE_DIRS} ${Tensorflow_INCLUDE_DIRS}/external/nsync/public)

set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -ffast-math")

# in the following, NDEBUG is set to avoid issues with constexpr in absl's string_view.h
set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -arch=sm_86 --expt-relaxed-constexpr -DNDEBUG")

add_library(
    rasterise SHARED
    rasterise_egl.cpp rasterise_egl.cu
    rasterise_grad_egl.cpp rasterise_grad_egl.cu rasterise_grad_common.h
    shaders.cpp shaders.h
    gl_dispatcher.h concurrentqueue.h blockingconcurrentqueue.h gl_common.h tf_cuda_utils.h hwc.h
)

target_compile_features(rasterise PUBLIC cxx_std_11)
target_compile_options(rasterise PUBLIC ${Tensorflow_COMPILE_FLAGS})
target_link_libraries(rasterise OpenGL::EGL OpenGL::OpenGL ${Tensorflow_LINK_FLAGS})
target_link_libraries(rasterise ${TENSORFLOW_INSTALL_PATH}/libtensorflow_framework.so.1)  # Adjust the library name as per your system
target_link_libraries(rasterise cuda)
# Put the compiled library in the python package folder, rather than whatever build folder is being used
set_target_properties(
    rasterise PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../dirt
)
