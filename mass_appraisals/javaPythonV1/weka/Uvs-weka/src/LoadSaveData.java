import weka.core.Instances;
import weka.core.converters.ArffSaver;

import java.util.*;
import java.util.List;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.FileNotFoundException;

public class LoadSaveData {

	public static void main(String[] args) throws Exception {
		
		String File = "/Users/sam/Github/Recommender-platform/mass_appraisals/javaPythonV1/python/inmuebles_casas_nivel_medio_entidad_cdmx_1_de_72.arff";
		loadArff(File);
		
		
		
	}
	
	
	public static Instances loadArff(String fileName) throws Exception{
		Instances dataset = new Instances(new BufferedReader(new FileReader(fileName)));
		Boolean var_show = false;
		
		if (var_show){
			System.out.println(dataset.toSummaryString());
					
			String rel_name = dataset.relationName();
			System.out.println("Numero de ejemplos en cluster: " + rel_name);

			int num_instances = dataset.numInstances();
			System.out.println("Numero de ejemplos en cluster: " + Integer.toString(num_instances));
			
			int avgConclu = (int) dataset.meanOrMode(35);
			System.out.println("Promedio importe concluido: " + Integer.toString(avgConclu));
			int stdDerConclu = (int) Math.sqrt(dataset.variance(35));
			System.out.println("Desviación importe concluido: " + Integer.toString(stdDerConclu));
					
			int avgM2 = (int) dataset.meanOrMode(34);
			System.out.println("Promedio importe m2: " + Integer.toString(avgM2));
			int stdDerM2 = (int) Math.sqrt(dataset.variance(34));
			System.out.println("Desviación importe m2: " + Integer.toString(stdDerM2));
			
			int stdDerLat = (int) (Math.sqrt(dataset.variance(1))*111320);
			System.out.println("Desviación latitud: " + Integer.toString(stdDerLat));
			int stdDerLong = (int) (Math.sqrt(dataset.variance(0))*111320);
			System.out.println("Desviación longitud: " + Integer.toString(stdDerLong));
			
		}
		
		
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
