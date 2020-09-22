package markov;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Collection;
import java.util.List;

import CbrQuerys.CBR;
import markov.ParaJSONFile;
import cbr.cbrDescriptions.TrucoDescription;
import jcolibri.exception.ExecutionException;
import jcolibri.method.retrieve.RetrievalResult;

public class RespondeMarkovEngine implements CBR {
	static String pasta = "C:/Users/LanaR/eclipse-workspace/clustercbrgamer/src/markov/";
	
	@Override
	public boolean aceitarEnvido(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptEnvido.py", 0.4f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean chamarEnvido(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptEnvido.py", 0.4f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean chamarRealEnvido(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptEnvido.py", 0.6f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean chamarFaltaEnvido(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptEnvido.py", 0.8f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean aceitarRealEnvido(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptEnvido.py", 0.6f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean aceitarFaltaEnvido(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptEnvido.py", 0.8f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean chamarTruco(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptTruco.py", 0.5f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean chamarReTruco(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptTruco.py", 0.7f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean chamarValeQuatro(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptTruco.py", 0.8f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean aceitarTruco(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptTruco.py", 0.5f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean aceitarReTruco(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptTruco.py", 0.7f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean aceitarValeQuatro(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptTruco.py", 0.8f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	/*
	 * Cartas retorna o id
	 */
	@Override
	public int primeiraCarta(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "0";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptProximaCarta.py", 0.1f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return Integer.parseInt(respostaFinal);
	}

	@Override
	public int segundaCarta(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "0";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptProximaCarta.py", 0.2f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return Integer.parseInt(respostaFinal);
	}

	@Override
	public int terceiraCarta(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "0";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptProximaCarta.py", 0.3f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return Integer.parseInt(respostaFinal);
	}

	@Override
	public boolean cartaVirada(TrucoDescription gameStateRobo, int rodada) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public boolean aceitarContraFlor(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptContraFlor.py", 0.6f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean aceitarContraFlorResto(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptContraFlor.py", 0.8f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean chamarContraFlor(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptContraFlor.py", 0.6f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean chamarContraFlorResto(TrucoDescription gameStateRobo, int rodada) {
		String respostaFinal = "false";
		try {
			respostaFinal = fazConsulta(gameStateRobo, rodada, pasta + "scriptContraFlor.py", 0.8f);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return respostaFinal.equals("true");
	}

	@Override
	public boolean irAoBaralho(TrucoDescription gameStateRobo, int rodada) {
		// TODO Auto-generated method stub
		return false;
	}
	
	public static String fazConsulta(TrucoDescription gameStateRobo, int rodada, String script, float probabilidade) throws IOException {
		Runtime rt = Runtime.getRuntime();
	    ParaJSONFile file = new ParaJSONFile(gameStateRobo);
	    
	    file.converteParaJSON();
	    Process proc = rt.exec("python " + script + " " + rodada + " " + probabilidade);

	    BufferedReader stdInput = new BufferedReader(new InputStreamReader(proc.getInputStream()));
	    BufferedReader stdError = new BufferedReader(new InputStreamReader(proc.getErrorStream()));

	    String answer = new String();
	    String finalAnswer = answer;
		while ((answer = stdInput.readLine()) != null) {
			finalAnswer = answer;
	        //System.out.println(finalAnswer);
	    }
		
		String error = new String();
	    String finalError = error;
		while ((error = stdError.readLine()) != null) {
			finalError = error;
	        System.out.println(finalError);
	    }
		if (!finalError.isEmpty())
			System.exit(0);
	    
	    return finalAnswer;	
	}
	
/*
 * aqui você recebe as informações com o que vc precisa
 * quem ganhou, pontuação ....Esse método passa o agente que você quiser de forma invertida, me pergunta que eu te explico.
 */
	@Override
	public void retain(TrucoDescription newCase) { 
		Runtime rt = Runtime.getRuntime();
		ParaJSONFile file = new ParaJSONFile(newCase);
		String script = pasta + "script.py";
		 
		file.converteParaJSON();
		try {
			Process proc = rt.exec("python " + script);

			BufferedReader stdInput = new BufferedReader(new InputStreamReader(proc.getInputStream()));
		    BufferedReader stdError = new BufferedReader(new InputStreamReader(proc.getErrorStream()));
		    
		    String answer = new String();
		    String finalAnswer = answer;
			while ((answer = stdInput.readLine()) != null) {
				finalAnswer = answer;
		        //System.out.println(finalAnswer);
		    }
			
			String error = new String();
		    String finalError = error;
			while ((error = stdError.readLine()) != null) {
				finalError = error;
		        System.out.println(finalError); 
		    }
			if (!finalError.isEmpty())
				System.exit(0);
			//Thread.sleep(2000);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} //catch (InterruptedException e) {
			// TODO Auto-generated catch block
			//e.printStackTrace();
		//}
		
	}

	@Override
	public Collection<RetrievalResult> retornaRecuperadosFiltradoPontos(TrucoDescription gamestate, double threshold) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Collection<RetrievalResult> retornaRecuperadosFiltradosTruco(TrucoDescription gamestate, double threshold,
			int rodada) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Collection<RetrievalResult> retornaRecuperadosFiltradosPrimeiraCarta(TrucoDescription gamestate,
			double threshold, int jogadorMao) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public List<TrucoDescription> retornaRecuperadosFiltradosSegundaCarta(TrucoDescription gamestate,
			double threshold) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Collection<RetrievalResult> retornaRecuperadosFiltradosTerceiraCarta(TrucoDescription gamestate,
			double threshold) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public boolean selecaoJogada(int Nao, int SimGanhou, int SimPerdeu) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public boolean selecaoJogadaVitoria(int Ganhou, int Perdeu) {
		// TODO Auto-generated method stub
		return false;
	}


	@Override
	public void setAprendizagem(String tipo) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void setRetencao(String tipo) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void fechaBase() throws ExecutionException {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void realizaConfiguracoesIniciais() {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void setThreshold(double threshold) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public double getThreshold() {
		// TODO Auto-generated method stub
		return 0;
	}

	@Override
	public boolean faltaConhecimentoParaAdecisao(TrucoDescription query, String tipoDaConsulta) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public void zeraGruposInformacoesRodadaFinalizada() {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void setTipoDecisao(String Tipo1, String tipoReusoIntraCluster1) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void setReusoComCluster(boolean cluster) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void setaGrupoMaisSimilarIndexadoJogada(TrucoDescription stateAgent1Jogada) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void setaGrupoMaisSimilarIndexadoPontos(TrucoDescription stateAgent1Envido) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void setAjusteAutomaticoDoK(boolean ajusteAutomaticoDoK) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void autoAjustarK() {
		// TODO Auto-generated method stub
		
	}

}
