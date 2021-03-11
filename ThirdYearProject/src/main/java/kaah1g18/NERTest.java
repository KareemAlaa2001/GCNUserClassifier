package kaah1g18;

import java.util.ArrayList;
import edu.stanford.nlp.simple.*;

public class NERTest {
    public static void main(String[] args) {
        // Create a document. No computation is done yet.
        Document doc = new Document("Constructing a sentence where Kareem Hussein, who works at Tesco in Welwyn, studies at the University of Southampton, likes to visit youtube.com and was born on 03/01/2001 8 hours after midday is not very hard. I have a twitter handle of @KareemAlaa2001, and my email is asdf54@gmail.com, which didn't get picked up?");
        for (Sentence sent : doc.sentences()) {  // Will iterate over the only sentence lmao
            // // We're only asking for words -- no need to load any models yet
            // System.out.println("The second word of the sentence '" + sent + "' is " + sent.word(1));
            // // When we ask for the lemma, it will load and run the part of speech tagger
            // System.out.println("The third lemma of the sentence '" + sent + "' is " + sent.lemma(2));
            // // When we ask for the parse, it will load and run the parser
            // System.out.println("The parse of the sentence '" + sent + "' is " + sent.parse());
            // // ...
            System.out.println("NER Tags in this sentence: " + sent.nerTags());
        }
    }
}
