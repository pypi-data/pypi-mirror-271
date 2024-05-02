from pydantic import BaseModel


class ClipInterface(BaseModel):
    """Interface that describes a clip"""

    id: int
    url: str
    duration: int
    # Represents the transcript of the non-extended clip
    transcript: str
    # TODO: Deprecate after the trimmer feature
    transcription: str

    def to_dict(self):
        return {
            "id": self.id,
            "transcript": self.transcript,
            "transcription": self.transcription,
            "url": self.url,
            "duration": self.duration,
        }
