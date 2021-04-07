from corpusreader import CorpusReader, FileExtractor


def main():
    fextractor = FileExtractor("XML")
    # posts = fextractor.extractData("../../datasets/meta.stackoverflow.com/Posts.xml")
    # comments = fextractor.extractData("../../datasets/meta.stackoverflow.com/Comments.xml")
    # users = fextractor.extractData("../../datasets/meta.stackoverflow.com/Users.xml")

    reader = CorpusReader(False)
    # reader.readCorpus() # TODO implement this whole setup out with the SO_ds and make it happennnn




if __name__ == '__main__':
    main()