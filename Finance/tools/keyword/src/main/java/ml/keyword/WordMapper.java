package ml.keyword;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class WordMapper extends Mapper<LongWritable,Text,Text,IntWritable>{

	private static final IntWritable one = new IntWritable(1);

	@Override
	protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, Text, IntWritable>.Context context)
			throws IOException, InterruptedException {
		String line = value.toString();
		line = line.replaceAll("[^\\p{L}\\p{Z}]", " ");
		
		String[] tokens = line.split(" ");
		
		//String description = tokens[3];
		
		for(String s : tokens) {
			if(!s.matches(".*\\d.*")) {
				context.write(new Text(s+","), one);
			}
		}
	}

}
