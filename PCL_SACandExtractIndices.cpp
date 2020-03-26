#include <ros/ros.h>
#include <pcl_ros/point_cloud.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <iostream>
#include <pcl/filters/passthrough.h>
#include <pcl/ModelCoefficients.h>
#include <pcl/io/pcd_io.h>
#include <pcl/filters/extract_indices.h>

ros::Publisher pub;
ros::Publisher pub1;

void cloud_cb (const sensor_msgs::PointCloud2ConstPtr& input)
{
 /* 
  pcl::PCLPointCloud2* cloud = new pcl::PCLPointCloud2; 
  pcl::PCLPointCloud2ConstPtr cloudPtr(cloud);
  pcl::PCLPointCloud2 cloud_filtered;

  pcl_conversions::toPCL(*cloud_msg, *cloud);
 
  pcl::PassThrough<pcl::PCLPointCloud2> pass;
//  pcl::PassThrough<PointType> pass (true);
  pass.setInputCloud (cloudPtr);
  pass.setFilterFieldName ("y");
  pass.setFilterLimits (0.01, 100.0);
  pass.setFilterLimitsNegative (true);
  pass.filter (cloud_filtered);

  sensor_msgs::PointCloud2 output;
  pcl_conversions::fromPCL(cloud_filtered, output);
*/

  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_p (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_f (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
  
  pcl::fromROSMsg(*input, *cloud);
  
  pcl::ModelCoefficients::Ptr coefficients (new pcl::ModelCoefficients);
  pcl::PointIndices::Ptr inliers (new pcl::PointIndices);

//SAC SEGMENTATION

  pcl::SACSegmentation<pcl::PointXYZ> seg;
  seg.setOptimizeCoefficients (true);
  seg.setModelType(pcl::SACMODEL_PLANE);
  seg.setMethodType(pcl::SAC_RANSAC);
  seg.setDistanceThreshold (0.01);
 
  
//EXTRACTION 
  
  pcl::ExtractIndices<pcl::PointXYZ> extract;
  
  int i = 0, nr_points = (int) cloud->points.size ();
  // While 30% of the original cloud is still there
  
while (cloud->points.size () > 0.3 * nr_points)
  {
    // Segment the largest planar component from the remaining cloud
    seg.setInputCloud (cloud);
    seg.segment (*inliers, *coefficients);

    // Extract the inliers
    extract.setInputCloud (cloud);
    extract.setIndices (inliers);
    extract.setNegative (false);
    extract.filter (*cloud_p);
     
    extract.setNegative (true);
    extract.filter (*cloud_f);
    cloud.swap (cloud_f);
    
    i++;
  }
  
  pub1.publish(*cloud_f);

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
  pub = nh.advertise<pcl_msgs::ModelCoefficients> ("/model_coeff", 1);
  // Spin
  ros::spin ();
}
