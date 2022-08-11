cmake_minimum_required(VERSION 2.8.3)

project(luminous_description)

find_package(catkin REQUIRED COMPONENTS roscpp rospy std_msgs)

include_directories(${catkin_INCLUDE_DIRS})


catkin_package()

find_package(roslaunch)


foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)
