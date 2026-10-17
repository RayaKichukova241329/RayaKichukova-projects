# Business understanding

Market research and problem definition for the face shape tool. This is an anonymised, condensed version of the report I wrote for the course.

## Problem

Shoppers cannot try frames on when buying eyewear online, so they are unsure how a pair will fit or look. That uncertainty leads to returns, frustration and lost sales.

- Online purchases are returned **17.6%** of the time, against about 10% in physical stores, and eyewear is among the most returned items because of fit (Vision Monday).
- The e-commerce eyewear market is projected to grow from **$45.8 billion in 2023 to $98.6 billion by 2033**, a growth rate of about 7.9% a year (Global Insight Services).
- The virtual fitting room market was valued at **$4.9 billion in 2023** and is expected to grow about 23.9% a year (Polaris Market Research).
- Personalised recommendations make customers 2.4 times more likely to complete a purchase (Arbelle AI), and effective personalisation has been linked to a 20% increase in conversion (Banuba).

## The gap

Large brands such as Warby Parker, Zenni Optical and Ray-Ban already use AI recommendations. Many small and mid-sized retailers, especially in Eastern Europe (Bulgaria, Romania, Portugal and Greece were the examples I used), cannot afford them. Augmented reality try-on is costly, from about $3,000 for a basic version to more than $10,000 for an advanced one (HQSoftware), and it needs camera access, which raises privacy concerns. Many shops still offer only filters such as colour and material.

**Problem definition:** online eyewear shoppers lack a way to judge fit, and small retailers lack an affordable, privacy-conscious tool that works from a static photo and recommends frames for the shopper's face shape.

## Stakeholders

Power-interest matrix:

| | Low interest | High interest |
|---|---|---|
| **High power** | **Context setters**: investors and regulators (GDPR, AI ethics) | **Players**: small and mid-sized retailers in underserved markets |
| **Low power** | **Crowd**: offline stores | **Subjects**: consumers who buy eyewear online |

The main stakeholder is the **small and mid-sized retailer**: they implement the tool and gain the most, and they need an affordable solution with easy integration and a clear return on investment. The tool lets them compete with larger brands, lowers return costs and improves customer retention.

## Data-analytic problem (DAPS)

- **Prediction:** a user's face shape (heart, round or square), and from it suitable eyewear styles.
- **Decision:** the model recommends, and users and retailers can accept, refine or override. Decisions happen instantly when a photo is uploaded, and periodically for retailers' inventory planning.
- **Type of relationship:** correlational and deductive (for example, square frames suit round faces), not causal.
- **Possible predictors:** facial landmarks and proportions such as jawline width, forehead ratio and cheekbone prominence; image features; user preferences; market trends.

## The idea

An AI tool that analyses facial proportions from a photo and recommends frame styles, aimed first at Eastern European retailers, where such tools are rare. It reduces returns, increases consumer confidence and gives smaller retailers a competitive advantage.

## Sources

Global Insight Services, Vision Monday, Polaris Market Research, Arbelle AI, Banuba, Statista and HQSoftware, as listed in the original report. An AI language model was used for grammar and spelling.

Back to the [project README](../README.md).
