import weka.core.Instances;
import weka.core.converters.ArffSaver;

import java.util.*;
import java.util.List;
import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileNotFoundException;

public class LoadSaveData {

	public static void main(String[] args) throws Exception {
		
		String File = "/Users/sam/Github/Recommender-platform/mass_appraisals/java/arffs/filtros_cubo_cdmx_departamentos_media33.arff";
		loadArff(File);

	}
	
	
	public static Instances loadArff(String fileName) throws Exception{
		Instances dataset = new Instances(new BufferedReader(new FileReader(fileName)));
		return dataset;
	}
	
	
	public static List<String> loadClusterFileNames(String namesFile){
		BufferedReader br;
		List<String> clusterNames = new ArrayList<String>();
        try {
            br = new BufferedReader(new FileReader(namesFile));
            try {
                String x;
                while ( (x = br.readLine()) != null ) {
                    // printing out each line in the file
                	//System.out.println(x);
                    clusterNames.add(x);
                } 
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (FileNotFoundException e) {
            System.out.println(e);
            e.printStackTrace();
        }
        
        return clusterNames;
		
		
	}

}
