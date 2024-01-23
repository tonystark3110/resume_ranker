import spacy
from PyPDF2 import PdfReader

class ResumeRanker:
    def __init__(self, criteria_keywords):
        try:
            # Use a larger model with word vectors
            self.nlp = spacy.load("en_core_web_lg")
        except IOError:
            spacy.cli.download("en_core_web_lg")
            self.nlp = spacy.load("en_core_web_lg")
        self.criteria_keywords = criteria_keywords

    def rank_resume(self, resume):
        total_score = 0

        for criterion, keywords in self.criteria_keywords.items():
            if criterion in resume:
                doc = self.nlp(resume[criterion])
                for keyword in keywords:
                    # Use similarity only if both tokens have vectors
                    if doc.has_vector and self.nlp(keyword).has_vector:
                        keyword_similarity = doc.similarity(self.nlp(keyword))
                        total_score += keyword_similarity

        return total_score

def read_resume_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return {'text': text}

# Example usage:
if __name__ == "__main__":
    # Define criteria keywords for the company
    criteria_keywords = {
        'text': ['aa', 'ff', 'Data Mining', 'gg', 'bob', 'jack', 'ff', 'Cloud Computing'],
    }

    # Specify the path to the resume file (PDF in this case)
    resume_file_path = r'C:/Users/Manikandan/Desktop/RESUMEEEEEEEE/Resume.pdf'

    # Read resume from the PDF file
    resume = read_resume_from_pdf(resume_file_path)

    # Create an instance of ResumeRanker
    ranker = ResumeRanker(criteria_keywords)

    # Rank the resume
    rank = ranker.rank_resume(resume)

    # Print the rank
    print(f"Resume Rank: {rank}")
