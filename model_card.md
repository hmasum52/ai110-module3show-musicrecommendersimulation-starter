# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MoodMatch 1.0**

---

## 2. Intended Use  

- **What kind of recommendations does it generate:** It scores every song in an 18-song catalog against a user profile and returns the top-K matches ranked by a weighted sum of genre, mood, energy, and acousticness similarity.

- **What assumptions does it make about the user:** It assumes the user can articulate a single favorite genre, a single favorite mood, a target energy level (0–1), and a binary acoustic preference — with optional related genres and moods for partial credit.

- **Is this for real users or classroom exploration:** This is a classroom simulation; the catalog is too small and the preference model too rigid for real-world deployment, but it clearly illustrates how content-based filtering works.

---

## 3. How the Model Works  

- **What features of each song are used:** Each song is described by its genre, mood, energy level (how intense it feels), and acousticness (how "live" or instrument-forward it sounds).

- **What user preferences are considered:** The user states a favorite genre and mood, a target energy level, whether they like acoustic music, and optional lists of related genres and moods they'd also enjoy.

- **How does the model turn those into a score:** It compares each song to the user's preferences across all four features, gives each comparison a 0–1 score, then adds them up with genre weighted most heavily — the closer the match, the higher the final score.

- **What changes did you make from the starter logic:** Acousticness scoring was added as a fourth feature, and `related_genres` / `related_moods` lists were introduced so near-miss songs earn partial credit (0.5) instead of scoring zero.

---

## 4. Data  

- **How many songs are in the catalog:** 18 songs, each with a unique genre, artist, and set of audio attributes.

- **What genres or moods are represented:** 15 genres including lofi, pop, rock, jazz, classical, metal, folk, synthwave, and more; 14 moods ranging from chill and happy to dark, dramatic, and triumphant.

- **Did you add or remove data:** No songs were added or removed from the starter dataset.

- **Are there parts of musical taste missing in the dataset:** Yes — genres like reggae, hip-hop, R&B, and electronic pop are absent, and moods like nostalgic, romantic, or anxious have no representation, limiting the system for users with those preferences.

---

## 5. Strengths  

- **User types for which it gives reasonable results:** Users with clear, consistent preferences — like a study/focus listener who wants low-energy acoustic lofi — get tightly clustered, intuitive top results with scores above 0.85.

- **Any patterns you think your scoring captures correctly:** The three-tier genre/mood rule (exact → related → miss) correctly surfaces near-miss songs like ambient for a lofi user, rather than treating every non-exact genre as equally irrelevant.

- **Cases where the recommendations matched your intuition:** The Workout/Hype profile correctly ranked Gym Hero #1 and pulled in high-energy related genres (rock, techno, metal) for the remaining slots, matching what a real workout playlist would look like.

---

## 6. Limitations and Bias 

- **Features it does not consider:** The system ignores tempo, danceability, valence, and listening history, so two songs with identical genre and mood but very different sonic feel are treated as equal matches.

- **Genres or moods that are underrepresented:** 13 of 15 genres have exactly one song in the catalog, meaning users who prefer jazz, classical, or folk receive far fewer competitive matches than lofi or pop users who have 2–3 songs each.

- **Cases where the system overfits to one preference:** Because genre carries 0.44 of the total weight, a user with a strong genre preference will see the same 1–3 songs dominate every recommendation list regardless of how poorly they match on energy or mood.

- **Ways the scoring might unintentionally favor some users:** Users whose favorite genre happens to be well-represented in the catalog (lofi, pop) get more diverse top-5 results, while niche-genre users are structurally disadvantaged — an artifact of catalog size, not preference quality.

---

## 7. Evaluation  

- **Which user profiles you tested:** Three realistic profiles (Study/Focus, Workout/Hype, Late-Night Drive) and five adversarial profiles designed to expose edge cases, including a user whose favorite genre doesn't exist in the catalog and one with directly contradictory mood and energy preferences.

- **What you looked for in the recommendations:** Whether the top-ranked songs matched the user's stated genre and mood, and whether the score gap between #1 and #2 was meaningful or artificially inflated.

- **What surprised you:** The "Loud Silence" profile (peaceful mood, energy 0.97) still returned Velvet Cathedral at #1 — the combined genre+mood weight (0.66) was large enough to overcome a near-worst energy score of 0.21.

- **Any simple tests or comparisons you ran:** A weight-swap experiment (genre ↔ energy weights) confirmed that high-energy songs began separating in rank and the score cliff between #1 and #2 shrank noticeably, validating that genre dominance is the primary driver of filter-bubble behavior.

No need for numeric metrics unless you created some.

---

## 8. Future Work  

- **Additional features or preferences:** Incorporate tempo range, valence (musical positivity), and danceability into scoring so two songs with the same genre and mood but different sonic feel are no longer treated as equal.

- **Better ways to explain recommendations:** Show a per-feature score breakdown in the output (e.g. "genre: 1.0 | mood: 0.5 | energy: 0.88") so users can see exactly why each song ranked where it did, including the silent acoustic penalty.

- **Improving diversity among the top results:** Add a re-ranking step that penalizes back-to-back songs from the same artist or genre, preventing a single well-represented genre like lofi from occupying all five slots.

- **Handling more complex user tastes:** Support multiple taste profiles per user (e.g. "morning mode" vs "gym mode") and let users rate past recommendations so the weights adapt over time instead of staying fixed. 

---

## 9. Personal Reflection  

- **What you learned about recommender systems:** Even a simple weighted scoring formula encodes strong assumptions — the choice of weights is itself a design decision that determines whose preferences the system serves best.

- **Something unexpected or interesting you discovered:** The "Loud Silence" adversarial profile showed that genre and mood weights are so dominant (0.66 combined) that they can keep the "right" song at #1 even when its energy score is near-worst — which is both a strength and a bias.

- **How this changed the way you think about music recommendation apps:** It made the invisible levers in apps like Spotify feel more concrete — every time a playlist feels surprisingly on-point or weirdly repetitive, there's a weight somewhere behind it nudging the results in that direction.
