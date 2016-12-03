
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.PrintWriter;

import weka.*;
import weka.filters.supervised.attribute.AttributeSelection;
import weka.attributeSelection.ReliefFAttributeEval;
import weka.attributeSelection.CfsSubsetEval;
import weka.attributeSelection.Ranker;
import weka.attributeSelection.GreedyStepwise;

import weka.classifiers.functions.LinearRegression;
import weka.classifiers.functions.SMOreg;
import weka.classifiers.functions.MultilayerPerceptron;

import weka.classifiers.Evaluation;
import java.util.Random;

import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;
import weka.core.Instances;


import java.util.*;
import java.util.List;


public class go4itEngine {

	public static void main(String[] args) throws Exception{
		System.out.println("hola java-weka");
		
		String File = "/Users/sam/Github/Recommender-platform/mass_appraisals/javaPythonV1/python/cluster_files_inmuebles_casas_nivel_semilujo_entidad_cdmx.txt";
		
		loadClusters(File); 
	}
	
	
	public static void loadClusters(String namesFile) throws Exception{
		
		List<String> clusterNames = LoadSaveData.loadClusterFileNames(namesFile);
		int i = 0;
		
		PrintWriter writer = new PrintWriter("/Users/sam/Github/Recommender-platform/mass_appraisals/javaPythonV1/python/resultados_casas_cdmx_semilujo.csv", "UTF-8");
		writer.println("NOMBRE_CLUSTER, NUM_AVALUOS, NUM_ATT, NUM_ATT_FILT, PROMEDIO_IMP_CONCLUIDO, DSVEST_IMP_CONCLUIDO, DSVEST_LAT, DSVEST_LONG, LR_ERROR_ABS_PROM, MSV_ERROR_ABS_PROM, RNA_ERROR_ABS_PROM, LR_ERROR_ABS_PROM_FILT, MSV_ERROR_ABS_PROM_FILT, RNA_ERROR_ABS_PROM_FILT, LR_ERROR_REL_ABS, MSV_ERROR_REL_ABS, RNA_ERROR_REL_ABS, LR_ERROR_REL_ABS_FILT, MSV_ERROR_REL_ABS_FILT, RNA_ERROR_REL_ABS_FILT, MEJOR_ATT_FILT, MEJOR_ALG");
		
		for (String clusterFileName : clusterNames) {
			//if (i<clusterNames.size()){
			if (i<20000){
				i++;
				System.out.println("::::::::::::::::::::: " +Integer.toString(i));
		        Instances dataset = LoadSaveData.loadArff(clusterFileName);
				int numInstances = dataset.numInstances();
				if (numInstances > 5){
					Instances filteredSimple = filterAttributesSimple(dataset);
					Instances filteredAtt = filterAttributes(filteredSimple);
					String values = "";
					
					//////////////////////// CSV STATS filteredSimple
					String rel_name = dataset.relationName();
					System.out.println("NOMBRE_CLUSTER: " + rel_name);
					values = values + rel_name + ", ";

					int num_instances = filteredSimple.numInstances();
					System.out.println("NUM_AVALUOS: " + Integer.toString(num_instances));
					values = values + Integer.toString(num_instances) + ", ";
					
					int num_att = filteredSimple.numAttributes();
					System.out.println("NUM_ATT: " + Integer.toString(num_att));
					values = values + Integer.toString(num_att) + ", ";
					
					int num_att_filt = filteredAtt.numAttributes();
					System.out.println("NUM_ATT_FILT: " + Integer.toString(num_att_filt));
					values = values + Integer.toString(num_att_filt) + ", ";
					
					int avgConclu = (int) dataset.meanOrMode(35);
					System.out.println("PROMEDIO_IMP_CONCLUIDO: " + Integer.toString(avgConclu));
					values = values + Integer.toString(avgConclu) + ", ";
					int stdDerConclu = (int) Math.sqrt(dataset.variance(35));
					System.out.println("DSVEST_IMP_CONCLUIDO: " + Integer.toString(stdDerConclu));
					values = values + Integer.toString(stdDerConclu) + ", ";
					int varIndex = (int) ((stdDerConclu/(double)avgConclu)*100);
					//System.out.println("COEFICIENTE_PORCENTUAL_DESV_ENTRE_PROMEDIO: " + Integer.toString(varIndex));
					
					int stdDerLat = (int) (Math.sqrt(dataset.variance(1))*111320);
					System.out.println("DSVEST_LAT: " + Integer.toString(stdDerLat));
					values = values + Integer.toString(stdDerLat) + ", ";
					int stdDerLong = (int) (Math.sqrt(dataset.variance(0))*111320);
					System.out.println("DSVEST_LONG: " + Integer.toString(stdDerLong));
					values = values + Integer.toString(stdDerLong) + ", ";
					int varArea = stdDerLat*stdDerLong;
					//System.out.println("LAT_LONG_STD_AREA: " + Integer.toString(varArea));
					
					
					Evaluation lr = evalLinearModel(filteredSimple);
					Evaluation lrAttFiltered = evalLinearModel(filteredAtt);
					
					Evaluation smo = evalSMOModel(filteredSimple);
					Evaluation smoAttFiltered = evalSMOModel(filteredAtt);
					
					Evaluation neuralNet = evalNeuralModel(filteredSimple);
					Evaluation neuralNetAttFiltered = evalNeuralModel(filteredAtt);
					
					
					System.out.println("LR_ERROR_ABS_PROM: " + Integer.toString((int)lr.meanAbsoluteError()));
					values = values + Integer.toString((int)lr.meanAbsoluteError()) + ", ";
					System.out.println("MSV_ERROR_ABS_PROM: " + Integer.toString((int)smo.meanAbsoluteError()));
					values = values + Integer.toString((int)smo.meanAbsoluteError()) + ", ";
					System.out.println("RNA_ERROR_ABS_PROM: " + Integer.toString((int)neuralNet.meanAbsoluteError()));
					values = values + Integer.toString((int)neuralNet.meanAbsoluteError()) + ", ";
					System.out.println("LR_ERROR_ABS_PROM_FILT: " + Integer.toString((int)lrAttFiltered.meanAbsoluteError()));
					values = values + Integer.toString((int)lrAttFiltered.meanAbsoluteError()) + ", ";
					System.out.println("MSV_ERROR_ABS_PROM_FILT: " + Integer.toString((int)smoAttFiltered.meanAbsoluteError()));
					values = values + Integer.toString((int)smoAttFiltered.meanAbsoluteError()) + ", ";
					System.out.println("RNA_ERROR_ABS_PROM_FILT: " + Integer.toString((int)neuralNetAttFiltered.meanAbsoluteError()));
					values = values + Integer.toString((int)neuralNetAttFiltered.meanAbsoluteError()) + ", ";
					System.out.println("LR_ERROR_REL_ABS: " + Integer.toString((int)lr.relativeAbsoluteError()));
					values = values + Integer.toString((int)lr.relativeAbsoluteError()) + ", ";
					System.out.println("MSV_ERROR_REL_ABS: " + Integer.toString((int)smo.relativeAbsoluteError()));
					values = values + Integer.toString((int)smo.relativeAbsoluteError()) + ", ";
					System.out.println("RNA_ERROR_REL_ABS: " + Integer.toString((int)neuralNet.relativeAbsoluteError()));
					values = values + Integer.toString((int)neuralNet.relativeAbsoluteError()) + ", ";
					System.out.println("LR_ERROR_REL_ABS_FILT: " + Integer.toString((int)lrAttFiltered.relativeAbsoluteError()));
					values = values + Integer.toString((int)lrAttFiltered.relativeAbsoluteError()) + ", ";
					System.out.println("MSV_ERROR_REL_ABS_FILT: " + Integer.toString((int)smoAttFiltered.relativeAbsoluteError()));
					values = values + Integer.toString((int)smoAttFiltered.relativeAbsoluteError()) + ", ";
					System.out.println("RNA_ERROR_REL_ABS_FILT: " + Integer.toString((int)neuralNetAttFiltered.relativeAbsoluteError()));
					values = values + Integer.toString((int)neuralNetAttFiltered.relativeAbsoluteError()) + ", ";
					
					double sum_rel_abs_error = lr.relativeAbsoluteError() + smo.relativeAbsoluteError() + neuralNet.relativeAbsoluteError();
					double sum_filt_rel_abs_error = lrAttFiltered.relativeAbsoluteError() + smoAttFiltered.relativeAbsoluteError() + neuralNetAttFiltered.relativeAbsoluteError();
					if (sum_rel_abs_error > sum_filt_rel_abs_error){
						System.out.println("MEJOR_ATT_FILT: " + "SI CONVIENE FILTRAR ATTRIBUTOS");
						values = values + "SI" + ", ";
					}else{
						System.out.println("MEJOR_ATT_FILT: " + "NO CONVIENE FILTRAR ATTRIBUTOS");
						values = values + "NO" + ", ";
					}
					
					double min_lr_error = Math.min(lr.relativeAbsoluteError(), lrAttFiltered.relativeAbsoluteError());
					double min_msv_error = Math.min(smo.relativeAbsoluteError(), smoAttFiltered.relativeAbsoluteError());
					double min_rna_error = Math.min(neuralNet.relativeAbsoluteError(), neuralNetAttFiltered.relativeAbsoluteError());
					double min_lr_msv = Math.min(min_lr_error, min_msv_error);
					double min_final = Math.min(min_lr_msv, min_rna_error);
					
					if (lr.relativeAbsoluteError() == min_final){
						System.out.println("MEJOR_ALG: " + "REG_LIN");
						values = values + "REG_LIN" ;
					}else if(lrAttFiltered.relativeAbsoluteError() == min_final){
						System.out.println("MEJOR_ALG: " + "REG_LIN_FILT");
						values = values + "REG_LIN_FILT" ;
					}else if(smo.relativeAbsoluteError() == min_final){
						System.out.println("MEJOR_ALG: " + "MAQ_SOP_VECT");
						values = values + "MAQ_SOP_VECT";
					}else if(smoAttFiltered.relativeAbsoluteError() == min_final){
						System.out.println("MEJOR_ALG: " + "MAQ_SOP_VECT_FILT");
						values = values + "MAQ_SOP_VECT_FILT" ;
					}else if(neuralNet.relativeAbsoluteError() == min_final){
						System.out.println("MEJOR_ALG: " + "REDES_NEURONALES");
						values = values + "REDES_NEURONALES" ;
					}else if(neuralNetAttFiltered.relativeAbsoluteError() == min_final){
						System.out.println("MEJOR_ALG: " + "REDES_NEURONALES_FILT");
						values = values + "REDES_NEURONALES_FILT" ;
					}
					
					System.out.println("valores: " + values);
					writer.println(values);
				}else{
					System.out.println("Cluster con muy pocos ejemplos:");
				}
				System.out.println(":::::::::::::::::::::");
			}else{
				break;
			}
		}
		writer.close();
	}
	
	public static Instances filterAttributes(Instances dataset) throws Exception{
		AttributeSelection filter = new AttributeSelection();
		CfsSubsetEval eval = new CfsSubsetEval();
		GreedyStepwise search = new GreedyStepwise();
		filter.setEvaluator(eval);
		filter.setSearch(search);
		filter.setInputFormat(dataset);
		Instances filteredDataset = Filter.useFilter(dataset, filter);
		return filteredDataset;
	}
	
	public static Instances filterAttributesSimple(Instances dataset) throws Exception{
		
		// quitar attributo 35: $m2
		String[] opts = new String[]{"-R", "1,2,3,4,5,33,35"};
		Remove remove = new Remove();
		remove.setOptions(opts);
		remove.setInputFormat(dataset);
		Instances filteredData = Filter.useFilter(dataset, remove);
		return filteredData;
	}
	
	
	
	
	
	
	
	
	
	

	public static LinearRegression buildLinearModel(Instances dataset) throws Exception{
			dataset.setClassIndex(dataset.numAttributes()-1);
			LinearRegression lr = new LinearRegression();
			lr.buildClassifier(dataset);
			return lr;
		}
	
	
	
	public static SMOreg buildSMOModel(Instances dataset) throws Exception{
		dataset.setClassIndex(dataset.numAttributes()-1);
		SMOreg smo = new SMOreg();
		smo.buildClassifier(dataset);
		return smo;
	}
	
	
	public static MultilayerPerceptron buildNeuralModel(Instances dataset) throws Exception{
		dataset.setClassIndex(dataset.numAttributes()-1);
		MultilayerPerceptron neuralNet = new MultilayerPerceptron();
		neuralNet.buildClassifier(dataset);
		return neuralNet;
	}
		
	

	public static Evaluation evalLinearModel(Instances dataset) throws Exception{
			dataset.setClassIndex(dataset.numAttributes()-1);
			LinearRegression lr = new LinearRegression();
			Evaluation eval = new Evaluation(dataset);
			int folds = 10;
			if (dataset.numInstances()<10){
				folds = dataset.numInstances();
			}
			eval.crossValidateModel(lr, dataset, folds, new Random(1));
			//System.out.println("Mean absolute error:     " + eval.meanAbsoluteError());
			//System.out.println("Relative absolute error: " + eval.relativeAbsoluteError());
			
			return eval;
		}
	
	
	
	public static Evaluation evalSMOModel(Instances dataset) throws Exception{
		dataset.setClassIndex(dataset.numAttributes()-1);
		SMOreg smo = new SMOreg();
		Evaluation eval = new Evaluation(dataset);
		int folds = 10;
		if (dataset.numInstances()<10){
			folds = dataset.numInstances();
		}		 
		eval.crossValidateModel(smo, dataset, folds, new Random(1));
		return eval;
	}
	
	
	public static Evaluation evalNeuralModel(Instances dataset) throws Exception{
		dataset.setClassIndex(dataset.numAttributes()-1);
		MultilayerPerceptron neuralNet = new MultilayerPerceptron();
		Evaluation eval = new Evaluation(dataset);
		int folds = 10;
		if (dataset.numInstances()<10){
			folds = dataset.numInstances();
		}
		eval.crossValidateModel(neuralNet, dataset, folds, new Random(1));
		return eval;
	}

}