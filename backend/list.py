from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key="sk_3a2b08f304b06448cd17bf4806f01e8f499d9d2b6fe93dac")

voices = client.voices.get_all()

print("RAW RESPONSE:")
print(voices)
