package kaah1g18;

import edu.stanford.nlp.coref.data.CorefChain;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.ie.util.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.semgraph.*;
import edu.stanford.nlp.trees.*;
import java.util.*;


public class BasicPipelineExample {

  public static String text = "Constructing a sentence where Kareem Hussein, who works at Tesco in Welwyn, studies at the University of Southampton, likes to visit youtube.com and was born on 03/01/2001 8 hours after midday is not very hard.";

  public static void main(String[] args) {
     // creates a StanfordCoreNLP object, with POS tagging, lemmatization, NER, parsing, and coreference resolution
     Properties props = new Properties();
     props.setProperty("annotators", "tokenize,ssplit,pos,lemma, ner");
     StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

    //  // read some text in the text variable
    //  String text = "...";

     // create an empty Annotation just with the given text
     Annotation document = new Annotation(text);

     // run all Annotators on this text
     pipeline.annotate(document);

     

  }

}

