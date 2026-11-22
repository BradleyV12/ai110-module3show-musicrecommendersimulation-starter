# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests the top 5 songs from a small catalog for one user, based on a favorite genre, a favorite mood, and a target energy level. It explains each pick in plain words.

It assumes the user has one clear taste: one genre, one mood, one energy level. It is built for **classroom exploration**, not for real users.

**Not intended for:**

- Real music apps or any product with real listeners.
- Judging or ranking artists.
- Learning anything about a person beyond three simple preferences.

---

## 3. How the Model Works

Think of it as a point game. Every song starts at zero points. Then:

- If the song's **genre** matches the user's favorite genre, it gets **2 points**.
- If the song's **mood** matches the user's favorite mood, it gets **1 point**.
- For **energy**, the closer the song is to the user's target, the more points it gets, up to **1 point**. A perfect match gets 1.0. A song that is far away gets close to 0.

The best possible score is 4.0. The system scores every song, sorts them from highest to lowest, and shows the top 5 with the reasons for each score.

**Changes from the starter:** I filled in the empty functions, made every score come with a list of reasons, and added an optional weights setting so I could run the weight-shift experiment.

---

## 4. Data

- **20 songs** in `data/songs.csv`. The 10 starter songs plus 10 extra songs.
- **Genres:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, electronic, country, r&b, metal, folk, hip hop, classical, reggae, indie rock, gospel.
- **Moods:** happy, chill, intense, relaxed, moody, focused, euphoric, nostalgic, romantic, angry, peaceful, confident, melancholy, uplifting.
- **Columns:** genre, mood, energy, tempo, valence, danceability, acousticness. Only genre, mood, and energy are used in scoring.
- **Missing:** lyrics, language, artist popularity, release year, and anything about what a user has already heard. Most genres have only one song, and lofi has three, so a lofi fan gets more choices than a fan of any other genre.

---

## 5. Strengths

- It works well for users with a clear, common taste. The Chill Lofi and Deep Intense Rock profiles got exactly the songs I expected at #1.
- The reasons list makes every result easy to understand. You can see exactly why a song ranked where it did.
- The energy rule captures "close to what I want" well. *Coffee Shop Stories* showed up for Chill Lofi purely because its energy fit, which makes sense.
- It handled the jazz / relaxed / medium-energy profile well, ranking *Coffee Shop Stories* first and *Island Breeze* second.

---

## 6. Limitations and Bias

The biggest weakness I found is that **genre has too much power**. In the "high energy + sad" test (genre classical, mood sad, energy 0.9), the top result was *Moonlit Sonata Remix*, a very quiet classical piece with energy 0.18. It scored 2.28 only because of its genre match, even though it is the opposite of high energy. No song in the catalog has the mood "sad", so the mood rule did nothing.

Other issues:

- **Exact matching only.** "Indie pop" gets no credit for pop, and "relaxed" gets no credit for "chill".
- **Small catalog.** *Gym Hero* (pop, intense) shows up for happy-pop users because it is one of only two pop songs. It matches the genre and has high energy, but the mood is a poor fit.
- **Unknown genres.** A k-pop fan gets no genre points at all, so their list is built only from mood and energy. The system quietly serves them worse results and never says so.
- **One taste per person.** Someone who likes both lofi and metal cannot be described.

---

## 7. Evaluation

**Profiles tested:**

1. Default Pop/Happy (genre pop, mood happy, energy 0.8)
2. High-Energy Pop (pop, intense, 0.93)
3. Chill Lofi (lofi, chill, 0.35)
4. Deep Intense Rock (rock, intense, 0.92)
5. Conflicting: high energy + sad (classical, sad, 0.9), an adversarial case
6. Genre not in catalog (k-pop, happy, 0.8), an adversarial case
7. Middle of the road (jazz, relaxed, 0.5), an edge case

I looked at whether the top result matched my intuition, whether the reasons made sense, and whether any song kept showing up everywhere.

**Terminal output for each profile:**

**Default Pop/Happy**

```text
=
```

**High-Energy Pop**

```text
=
```

**Chill Lofi**

```text
=
```

**Deep Intense Rock**

```text
=
```

**Conflicting (high energy + sad)**

```text
=
```

**Genre not in catalog (k-pop)**

```text
=
```

**Middle of the road**

```text
=
```

**Comparisons between profiles:**

- **Default Pop/Happy vs High-Energy Pop:** both are pop, but the first wants *happy* and the second wants *intense*. The top song changed from *Sunrise City* (bright, happy) to *Gym Hero* (loud, intense). This makes sense because the mood and the energy target both changed.
- **High-Energy Pop vs Deep Intense Rock:** both want intense, loud songs, so *Gym Hero* and *Storm Runner* both appear in each list. The genre match decides who is #1 (pop gives *Gym Hero*, rock gives *Storm Runner*). This is valid: the two profiles are asking for almost the same energy, and only the genre separates them.
- **Chill Lofi vs Deep Intense Rock:** the lists share nothing. Chill Lofi gets slow, acoustic songs around 0.3 to 0.4 energy, and Rock gets loud songs above 0.88. This is the clearest sign the energy rule works.
- **Default Pop/Happy vs Chill Lofi:** these are opposites on both genre and energy, and the results are completely different. Good.
- **Chill Lofi vs Middle of the road (jazz):** both prefer calm music, so *Coffee Shop Stories* and *Midnight Coding* appear in each list. The jazz profile also brings in *Island Breeze* and *Velvet Hours*, which sit at medium energy. That fits the higher energy target of 0.5.
- **Default Pop/Happy vs k-pop:** the lists are almost the same, except that *Gym Hero* disappears. With no genre points available, the happy mood and 0.8 energy pick the songs, so the results look a lot like the pop list without the pop. This shows how much of the pop list was driven by genre alone.
- **High-Energy Pop vs Conflicting (sad):** both want very high energy, and the high-energy songs show up in both lists. The conflicting profile is different because its #1 is a quiet classical song. This is the one result that does **not** make sense, and it shows the genre bonus overpowering the energy rule.

**What surprised me:** *Gym Hero* keeps showing up for people who just want happy pop. In plain words: the system sees "pop" and gives 2 free points, then sees a high energy number that is not far from the user's 0.8. It never checks that the song's mood is "intense", not "happy". Because there are only two pop songs, *Gym Hero* has nowhere else to go but #2.

**Weight-shift experiment (genre 2.0 to 1.0, energy 1.0 to 2.0):** the happy-pop list improved, since *Rooftop Lights* now beats *Gym Hero*. The Chill Lofi list barely changed. Overall it made the results **more accurate** for the happy-pop user and **just different** for the rest. The maximum score stayed at 4.0, so the scores are still comparable.

---

## 8. Future Work

- **Use more features.** Add valence, danceability, acousticness, and tempo, and use the `likes_acoustic` setting that already exists in `UserProfile`.
- **Give partial credit for close genres and moods.** For example, "indie pop" could earn half credit for "pop", and "chill" could earn some credit for "relaxed".
- **Improve diversity.** Stop the top 5 from being filled by near-identical songs, for example by limiting how many songs from one genre or artist can appear.
- **Handle mixed tastes.** Allow a user to have several favorite genres or moods, with different weights.

---

## 9. Personal Reflection

> ✏️ **YOU: rewrite this in your own words.** This is a draft to build from. Replace the details with your own experience, especially what *you* found surprising and where *you* had to double-check the AI.

The biggest thing I learned is that a recommender is just "score everything, then sort", and almost all of the interesting choices are in the scoring rule. Changing the genre weight from 2.0 to 1.0 changed which song came first, so the weights are really opinions built into the system.

I used an AI assistant to write the first version of the code, the profiles, and the explanations. It was fast, but I still had to check the output myself. For example, I needed to confirm that the scores in the terminal matched my own hand math, and I had to notice that a quiet classical song topping a "high energy" list was a real flaw, not a feature.

What surprised me most is how a few simple rules can feel like a real recommendation. When *Library Rain* came out first for the Chill Lofi profile, it felt "right", even though the system has no idea what music sounds like. It only compares numbers and labels.

If I kept going, I would add partial credit for similar genres and moods, use the other features, and test the system with a bigger, more balanced catalog. It also changed how I see music apps. When one feels like it "gets" me, it is probably doing a much bigger version of this same thing, and its designers made choices that shape what I hear.
