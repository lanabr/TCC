package markov;

import java.io.File;
import java.io.IOException;

import com.fasterxml.jackson.databind.ObjectMapper;

import cbr.cbrDescriptions.TrucoDescription;;

public class ParaJSONFile {
	private TrucoDescription estadoJogo;
	private File             fileJSON;
	private ObjectMapper     mapper;
	
	public ParaJSONFile(TrucoDescription jogoAtual) {
		this.estadoJogo     = jogoAtual;
		this.fileJSON       = new File("C:/Users/LanaR/eclipse-workspace/clustercbrgamer/src/markov/trucodescription.json");
		this.mapper         = new ObjectMapper();
	}

	public ObjectMapper getMapper() {
		return mapper;
	}

	public void setMapper(ObjectMapper mapper) {
		this.mapper = mapper;
	}

	public File getFileJSON() {
		return fileJSON;
	}

	public void setFileJSON(File fileJSON) {
		this.fileJSON = fileJSON;
	}

	public TrucoDescription getEstadoJogo() {
		return estadoJogo;
	}

	public void setEstadoJogo(TrucoDescription estadoJogo) {
		this.estadoJogo = estadoJogo;
	}
	
	public void converteParaJSON() {
		try {
			mapper.writeValue(fileJSON, estadoJogo);
		}catch (IOException e) {
            e.printStackTrace();
        }
	}

}
