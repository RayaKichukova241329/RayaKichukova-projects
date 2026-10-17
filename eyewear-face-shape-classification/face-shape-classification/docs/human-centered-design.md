# Human-centred design

How the model became an experience: the prototype, a think-aloud study and an A/B test. Participants are anonymised, and the recordings and transcripts are not published.

## Prototype

A clickable Figma prototype of an eyewear shop: open the page, upload a photo or take one, see your face shape with a short explanation, browse frame recommendations, save your results and return to the start.

- [Prototype, version A](https://www.figma.com/proto/24rY6Z9phTcSL2BrlVkAfO/Wireframe-2?page-id=2007%3A26&node-id=2007-27&p=f&scaling=scale-down&content-scaling=fixed&starting-point-node-id=2007%3A27)
- [Prototype, version B](https://www.figma.com/proto/eBRC6JGquHbeHSgxp620ox/Wireframe-2--Version-B-?page-id=2007%3A26&node-id=2007-27&starting-point-node-id=2007%3A27)

Design choices, tied to human-centred AI principles:

- **A soft, light purple accent** for a calm, welcoming look that suits a style-oriented tool, and to avoid pulling attention from the content (aesthetic and minimalist design).
- **No registration needed** to see results and browse recommendations, so users stay in control and are not pressured to commit.
- **Familiar patterns and clear labels**, with a visible way back to the home screen, so the interface is predictable and needs little recall.

## Think-aloud study

Three participants worked through the prototype as a persona: a busy professional who wants a fast way to find frames that suit their face shape without visiting a shop. They completed eight tasks (open the page, try the tool, upload or take a photo, read the result, save it, log in, view saved results, return to the start) and answered sixteen questions about first impressions, clarity, usefulness and ease of use.

I coded the sessions with a simple framework: understood what to do, was confused, did the right action, did the wrong action, suggested an improvement.

**Findings**

- **Intuitive interface:** every participant navigated with minimal guidance.
- **Prototype limits caused confusion:** one participant expected to upload their own photo and enter a name, which the prototype did not support.
- **Recommendations were the most valued part.** One participant suggested short explanations of why frames suit or do not suit a face shape.
- **Positive aesthetic feedback:** clean, modern and appealing.

**What I changed:** I added a registration page, because participants expected one, added short explanations to the results (frames that do or do not suit a face shape and why), and made clear in testing which features were not yet functional.

## A/B test

**Question:** does grouping frame recommendations into categories (version B) make the results clearer than the original layout (version A)?

**Method:** each participant was randomly assigned to one version and had up to four minutes to go from the home page through the face scan to the results and the frame recommendations, without guidance unless they were completely stuck. Afterwards they answered a Likert-scale survey.

**Results:** independent t-tests found no significant difference between versions on any question (all p-values above 0.05).

| Survey statement | p-value |
|---|---|
| I understood what I could use the app for. | 0.234 |
| I found the application intuitive to use. | 0.531 |
| I thought the application was useful. | 0.485 |
| I enjoyed using the application. | 0.822 |
| I found the eyewear categories helpful in making a choice. | 0.506 |

**Interpretation:** a lack of significance does not prove the grouping was useless. With this sample size and survey, any effect was too small to detect. Both versions were rated mostly positively, which supports the core design. I kept the design direction, and the next steps are a larger sample and a survey that measures the effect of specific interface elements more directly.

Back to the [project README](../README.md).
