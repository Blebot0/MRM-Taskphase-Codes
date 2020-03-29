#include <ros/ros.h>
#include <pcl_ros/point_cloud.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <iostream>
#include <pcl/ModelCoefficients.h>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/features/normal_3d.h>
#include <pcl/kdtree/kdtree.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/segmentation/extract_clusters.h>


ros::Publisher pub;
ros::Publisher pub2;
ros::Publisher pub1;


void cloud_cb (const sensor_msgs::PointCloud2ConstPtr& input)
{

  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_p (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_f (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_filtered (new pcl::PointCloud<pcl::PointXYZ>);

  pcl::fromROSMsg(*input, *cloud);
  
  pcl::ModelCoefficients::Ptr coefficients (new pcl::ModelCoefficients);
  pcl::PointIndices::Ptr inliers (new pcl::PointIndices);

//VOXEL
  pcl::VoxelGrid<pcl::PointXYZ> sor;
  sor.setInputCloud (cloud);
  sor.setLeafSize (0.01f, 0.01f, 0.01f);
  sor.filter (*cloud_filtered);

//SAC SEGMENTATION

  pcl::SACSegmentation<pcl::PointXYZ> seg;
  seg.setOptimizeCoefficients (true);
  seg.setModelType(pcl::SACMODEL_PLANE);
  seg.setMethodType(pcl::SAC_RANSAC);
  seg.setDistanceThreshold (0.01);
  seg.setMaxIterations (100);

//EXTRACTION 
  
  int i = 0, nr_points = (int) cloud_filtered->points.size (); 
while (cloud_filtered->points.size () > 0.8 * nr_points )
  {
       
    pcl::ExtractIndices<pcl::PointXYZ> extract;
    // Segment the largest planar component from the remaining cloud
    seg.setInputCloud (cloud_filtered);
    seg.segment (*inliers, *coefficients);

    // Extract the inliers
    extract.setInputCloud (cloud_filtered);
    extract.setIndices (inliers);
    extract.setNegative (false);
    extract.filter (*cloud_p);
    
    //inlier inversed
    extract.setNegative (true);
    extract.filter (*cloud_f);
    *cloud_filtered = *cloud_f;
    
    i++;
  }
  
  pub1.publish(*cloud_f);

 //KD TREE  
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ>);
  tree->setInputCloud (cloud_filtered);

  std::vector<pcl::PointIndices> cluster_indices;
  pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
  ec.setClusterTolerance (0.1); // 1cm
  ec.setMinClusterSize (100);
  ec.setMaxClusterSize (50000000);
  ec.setSearchMethod (tree);
  ec.setInputCloud (cloud_filtered);
  ec.extract (cluster_indices);

//CLUSTERING
  int j = 0;
  pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud_cluster (new pcl::PointCloud<pcl::PointXYZRGB>);	  
  
  for (std::vector<pcl::PointIndices>::const_iterator it = cluster_indices.begin (); it != cluster_indices.end (); ++it)
  {
    for (std::vector<int>::const_iterator pit = it->indices.begin (); pit != it->indices.end (); ++pit)
    {

	    pcl::PointXYZRGB point;
            point.x = cloud_filtered->points[*pit].x;
            point.y = cloud_filtered->points[*pit].y;
            point.z = cloud_filtered->points[*pit].z;

	    if (j == 0) //Red	#FF0000	(255,0,0)
			     {
				      point.r = 0;
				      point.g = 0;
				      point.b = 255;
			     }
			    else if (j == 1) //Lime	#00FF00	(0,255,0)
			     {
				      point.r = 0;
				      point.g = 255;
				      point.b = 0;
			     }
			    else if (j == 2) // Blue	#0000FF	(0,0,255)
			     {
				      point.r = 255;
				      point.g = 0;
				      point.b = 0;
			     }
			    else if (j == 3) // Yellow	#FFFF00	(255,255,0)
			     {
				      point.r = 255;
				      point.g = 255;
				      point.b = 0;
			     }
			    else if (j == 4) //Cyan	#00FFFF	(0,255,255)
			     {
				      point.r = 0;
				      point.g = 255;
				      point.b = 255;
			     }
			    else if (j == 5) // Magenta	#FF00FF	(255,0,255)
			     {
				      point.r = 255;
				      point.g = 0;
				      point.b = 255;
			     }
			    else if (j == 6) // Olive	#808000	(128,128,0)
		     	 {
				      point.r = 128;
				      point.g = 128;
				      point.b = 0;
			     }
			    else if (j == 7) // Teal	#008080	(0,128,128)
			     {
				      point.r = 0;
				      point.g = 128;
				      point.b = 128;
			     }
			    else if (j == 8) // Purple	#800080	(128,0,128)
		     	 {
				      point.r = 128;
				      point.g = 0;
				      point.b = 128;
			     }
			    else
		   	     {
				      if (j % 2 == 0)
				       {
					        point.r = 255 * j / (cluster_indices.size());
					        point.g = 128;
					        point.b = 50;
				       }
				      else
				       {
					        point.r = 0;
					        point.g = 255 * j / (cluster_indices.size());
					        point.b = 128;
				       }
                 }
	//    cloud_cluster->points.push_back (cloud_filtered->points[*pit]);
			    cloud_cluster->push_back(point);
    }

//    cloud_cluster->width = cloud_cluster->points.size ();
//    cloud_cluster->height = 1;
//    cloud_cluster->is_dense = true;
    
    j++;
  }

  cloud_cluster->header.frame_id = cloud->header.frame_id;
  pub2.publish(*cloud_cluster);
  
 std::cout<<j;
   // Publish the model coefficients
  pcl_msgs::ModelCoefficients ros_coefficients;
  pcl_conversions::fromPCL(*coefficients, ros_coefficients);
  pub.publish (ros_coefficients);

}





int main (int argc, char** argv)
{
  // Initialize ROS
  ros::init (argc, argv, "my_pcl_tutorial");
  ros::NodeHandle nh;

  // Create a ROS subscriber for the input point cloud
  ros::Subscriber sub = nh.subscribe ("input", 1, cloud_cb);

  // Create a ROS publisher for the output point cloud
//  pub = nh.advertise<sensor_msgs::PointCloud2> ("output", 1);
  pub1 = nh.advertise<pcl::PointCloud<pcl::PointXYZ> > ("/cloud_pcl", 100);
  pub2 = nh.advertise<pcl::PointCloud<pcl::PointXYZRGB> > ("/cloud_pcl/clustered", 10); 
  pub = nh.advertise<pcl_msgs::ModelCoefficients> ("/model_coeff", 1);
  // Spin
  ros::spin ();
}
