import streamlit as st
from word_sentiment_price import predict_sentiment_and_price
from datetime import date

# === Streamlit Page Setup ===
st.set_page_config(page_title="Natural Gas Predictor", layout="wide")

# === CSS Styling ===
st.markdown("""
    <style>
    .center-title {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stTextArea textarea {
        font-size: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# === Header ===
st.markdown('<div class="center-title">📊 Natural Gas Sentiment & Price Predictor</div>', unsafe_allow_html=True)
st.markdown("#### Enter a news article and publish date to analyze sentiment and predict natural gas price.")

## === Article Input Method Selection ===
input_mode = st.radio("Choose how you want to provide the article:", ["📝 Paste Article", "📚 Load Sample Article"])

# === Session State Initialization ===
if "article_text" not in st.session_state:
    st.session_state.article_text = ""

sample_articles = {
    "📰 LNG Canada and Depressed Prices in Western Canada": (
        "Natural gas producers in Western Canada have white-knuckled it through months of depressed prices, "
        "with the expectation that their fortunes will improve when LNG Canada comes online in the middle of next year. "
        "However, the supply glut is so significant that not everyone is convinced the facility’s impact on pricing will be dramatic or sustained. "
        "Spot prices have hovered between $1.20 and $1.60 per gigajoule, well below the 2023 average. "
        "Increased production, a mild winter, and full storage have all contributed to the low prices. "
        "While some companies like Advantage Energy are curtailing production, others continue growing in anticipation of LNG Canada's demand. "
        "LNG Canada is expected to process up to 2 Bcf/day, but experts warn that unless producers maintain discipline, "
        "the oversupply may return even after the facility starts operations in 2025."
    ),
    "📰 Cold Snap Drives Demand Amid Tight Supply": (
        "A cold snap across the Midwest and Northeast is driving soaring demand for heating, while supply remains tight "
        "due to ongoing pipeline maintenance and production slowdowns. Analysts warn of potential shortages if the weather persists."
    ),
    "📰 Mild Weather Boosts Natural Gas Storage Levels": (
        "Natural gas inventories are rising as mild weather dampens consumption and boosts storage levels. "
        "With demand remaining subdued, storage facilities are quickly filling, putting downward pressure on prices."
    ),
    "📰 Natural gas down 4% on profit-taking, ahead of bets for 'another rally'": (
        "Natural gas down 4% on profit-taking, ahead of bets for 'another rally' Natural gas down 4% on profit-taking, "
        "ahead of bets for 'another rally' Published Jun 27, 2023 03:48PM ET© Reuters.NG -2.97% Add to/Remove from WatchlistInvesting.com -- "
        "The bull run in natural gas paused Tuesday, giving back some 4% from a four-day rally. But analysts say the downside may not last, with demand for cooling likely to spike ahead of the July 4 Independence Day holiday which typically sees Americans partying at home and in their backyard as much as they take road trips.“The market seems to be in flux right now with the price rally losing some momentum likely due in part to profit taking by some market players,” analysts at Houston-based energy markets advisory Gelber & Associates said in a note to their clients in natural gas.But they also noted that “with the 4th of July happening in the middle of next week (Tuesday), producers are front loading maintenance to account for the holiday.”Plants undergo early maintenance to prepare for July 4 demand spikeGelber’s analysts estimate that about 1.5 billion cubic feet of daily gas production has been halted as plants underwent maintenance to prepare for ramped-up demand for the holiday and beyond, as summer progresses in earnest.The on the New York Mercantile Exchange’s Henry Hub settled down 10.3 cents, or 3.6%, at $2.789 per mmBtu, or metric million British thermal units.The session low was $2.76, retreating from Monday’s intraday high of $2.936, which marked the loftiest level for a front-month contract on the hub since March.It has been an interesting time for natural gas, with bulls managing to keep the market in the positive for four weeks in a row despite the U.S. Energy Information Administration, or EIA, reporting a higher-than-expected number for the fuel in the latest week.With a near 25% gain for June, gas futures are headed for their best month in almost a year. The last time the market rallied more in a month was in July 2022, when it gained 46%.While summer weather hasn’t hit its typical baking point across the country, cooling demand is inching up by the day, particularly in Texas. This has sparked realization in the trade that higher price lows might be more common than new bottoms.The lowest Henry Hub’s front-month got to in June was $2.138, versus its high of $2.935.100F temperature, high power burns, low gas output make another rally “probable”Temperatures in the South have reached 100+ degrees Fahrenheit earlier than expected and heat is expected to start permeating the entire lower 48 States in the coming weeks, Gelber’s analysts said earlier in the week.In Tuesday’s note, they emphasized the bullish fundamental support for natural gas as power demand continues to grow while production of dry gas production drops.“In addition to this, coal to gas fuel switching has been at record highs and will likely continue to be,” the analysts said, noting that power burns were likely to hit highs of more than 42 bcf per day on July 4.“This fundamental "
        "bullish support has largely offset market profit taking and a continued bull rally seems probable in the short term,” they added."
    ),

    "📰 Natural gas producers await LNG Canada's start": (
        "Natural gas producers await LNG Canada's start, but will it be the fix for prices? "
        "CALGARY — Natural gas producers in Western Canada have white-knuckled it through months of depressed prices, with the expectation that their fortunes will improve when LNG Canada comes online in the middle of next year. Natural gas producers in Western Canada have white-knuckled it through months of depressed prices with the expectation that their fortunes will soon improve when LNG Canada comes online in the middle of next year. A pumpjack draws out oil from a wellhead near Calgary on Saturday, Sept. 17, 2022. THE CANADIAN PRESS/Jeff McIntoshCALGARY — Natural gas producers in Western Canada have white-knuckled it through months of depressed prices, with the expectation that their fortunes will improve when LNG Canada comes online in the middle of next year.But the supply glut plaguing the industry this fall is so large that not everyone is convinced the massive facility's impact on pricing will be as dramatic or sustained as once hoped.As the colder temperatures set in and Canadians turn on their furnaces, natural gas producers in Alberta and B.C. are finally starting to see some improvement after months of low prices that prompted some companies to delay their growth plans or shut in production altogether." "We've pretty much been as low as you can go on natural gas prices. There were days when (the Alberta natural gas benchmark AECO price) was essentially pennies," 
        'It''s been pretty worthless'"In the past week, AECO spot prices have hovered between $1.20 and $1.60 per gigajoule, a significant improvement over last month's bottom-barrel prices but still well below the 2023 average price of $2.74 per gigajoule, according to Alberta Energy Regulator figures.The bearish prices have come due to a combination of increased production levels — up about six per cent year-over-year so far in 2024 —as well as last year's mild winter, which resulted in less natural gas consumption for heating purposes. There is now an oversupply of natural gas in Western Canada, so much so that natural gas storage capacity in Alberta is essentially full.Mike Belenkie, CEO of Calgary-headquartered natural gas producer Advantage Energy Ltd., said companies have been ramping up production in spite of the poor prices in order to get ahead of the opening of LNG Canada. The massive Shell-led project nearing completion near Kitimat, B.C. will be Canada's first large-scale liquefied natural gas export facility.It is expected to start operations in mid-2025, giving Western Canada's natural gas drillers a new market for their product.""In practical terms everyone’s aware that demand will increase dramatically in the coming year, thanks to LNG Canada . . . and as a result of that line of sight to increased demand, a lot of producers have been growing," "Belenkie said in an interview.""And so we have this temporary period of time where there’s more gas than there is places to put it.”In light of the current depressed prices, Advantage has started strategically curtailing its gas production by up to 130 million cubic feet per day, depending on what the spot market is doing.Other companies, including giants like Canadian Natural Resources Ltd. and Tourmaline Oil Corp., have indicated they will delay gas production growth plans until conditions improve.""We cut all our gas growth out of 2024, once we’d had that mild winter. We did that back in Q2, because this is not the right year to bring incremental molecules to AECO,"
        "said Mike Rose, CEO of Tourmaline, which is Canada's largest natural gas producer, in an interview this week.""We moved all our gas growth out into ’25 and ’26.”LNG Canada is expected to process up to 2 billion cubic feet (Bcf) of natural gas per day once it reaches full operations. That represents what will be a significant drawdown of the existing oversupply, Rose said, adding that is why he thinks the future for western Canadian natural gas producers is bright.""That sink of 2 Bcf a day will logically take three-plus years to fill. And then if LNG Canada Phase 2 happens, then obviously that’s even more positive," "Rose said.While Belenkie said he agrees LNG Canada will lift prices," "hes not as convinced as Rose that the benefits will be sustained for a long period of time.""Our thinking is that markets will be healthy for six months, a year, 18 months — whatever it is — and then after that 18 months, because prices will be healthy, supply will grow and probably overshoot demand again,"
        "he said, adding he's frustrated that more companies haven't done what Advantage has done and curtailed production in an effort to limit the oversupply in the market.“Frankly, we’ve been very disappointed to see how few other producers have chosen to shut in with gas prices this low. . . you’re basically dumping gas at a loss,"" Belenkie said.Feit, the analyst for Enverus, said there's no doubt LNG Canada's opening will be a major milestone that will help to support natural gas pricing in Western Canada. He added there are other Canadian LNG projects in the works that would also provide a boost in the longer-term, such as LNG Canada's proposed Phase 2, as well as potential increased demand from the proliferation of AI-related data centres and other power-hungry infrastructure.But Feit added that producers need to be disciplined and allow the market to balance in the near-term, otherwise supply levels could overshoot LNG Canada's capacity and periods of depressed pricing could reoccur.""Obviously selling gas at pennies on the dollar is not a sustainable business model,"" Feit said.""But there's an old industry saying that the cure for low gas prices is low gas prices. You know, eventually companies will have to curtail production, they will have to make adjustments.""This report by The Canadian Press was first published Oct. 25, 2024.Companies in this story: (TSX:TOU; TSX:AAV, TSX:CNQ)Amanda Stephenson, The Canadian Press"
    ),

    "📰 Volatile natural gas prices spark energy bill concerns": (
        "Cold weather in Europe has eaten into gas stocks, boosting prices and raising fears of higher energy bills. "
        "Natural gas was trading 25% higher in London compared to mid-December, which could affect both residential and industrial consumers."
    ),

    "📰 Biden’s LNG ‘pause’ threatens Pennsylvania’s gas exports": (
       "Biden’s LNG ‘pause’ threatens Pennsylvania’s natural gas industry The Biden administration’s political objectives coupled with the intense desire to implement green energy policies overnight are robbing Americans and our allies of a stable energy source as demand grows at home and abroad. During the 2020 election, then-candidate Joe Biden campaigned on ending fossil fuels. Now, his administration’s decision made in January — a so-called “pause” on pending liquified natural gas (LNG) exports — comes during an election year yet again. Except this time, the policy decision is effective immediately, and it dramatically threatens Pennsylvania’s flourishing natural gas industry.As the saying goes, “promises made, promises kept.”Pennsylvania is the second largest natural gas producing state in the country, behind only Texas, according to the U.S. Energy Information Administration (EIA). The Keystone State, what was once deemed “The Saudi Arabia of natural gas,” accounts for nearly one-fifth of the nation’s natural gas output. Compared to traditional natural gas that many of us use to heat our homes, LNG is natural gas that has been supercooled to a liquid state. This allows for easier shipping and storage, making it a hot commodity on the global energy market.The Biden administration announced this election-year pause citing climate change, doubling down on a promise to combat what the president calls the “existential threat of our time.”No one is against protecting the environment. In fact, that is one of the biggest benefits of natural gas — it is perhaps the cleanest fossil fuel on the market today. It is also abundant and affordable. That abundance is what propelled the United States to become the global leader in LNG exports in 2023, surpassing longtime leaders Qatar and Australia.America is not only competing — it is winning.But once again, the Biden administration is forcing short-sighted energy policy to fit broader political needs rather than what is in America’s best interest. Their track record on American energy leads me to believe that this “pause” may not be temporary after all. On Day One in office, Biden signed executive actions to cancel the Keystone XL pipeline project between the U.S. and Canada. Then, two years ago, the administration depleted nearly half of our national Strategic Petroleum Reserve (SPR) to lower gas prices after Russia’s invasion of Ukraine rattled the oil markets. These reserves are used for major natural disasters, such as hurricanes. Prices dropped a few cents each time oil was released ahead of the 2022 midterm elections, yet Americans still paid as much as $5 a gallon for gasoline. Despite a pledge to refill the reverses, they remain only half full.This is why, over the last month or so, House Republicans have passed legislation to reverse the administration’s decision. This includes a bill that would shift LNG export authority from the Department of Energy (DOE) to the Federal Energy Regulatory Commission (FERC). This would depoliticize the LNG export ban and allow for a more policy-driven discussion. Just last month, the House also passed the “Protecting American Energy Production Act,” legislation which prohibits the president from declaring a moratorium on hydraulic fracturing. In recent days, we have seen more than a dozen states take legislative and legal action of their own to reverse this economically-threatening pause.These House-passed bills are necessary because DOE has already commissioned five studies to examine the economic and environmental effects of U.S. LNG exports. Further, DOE has also issued two studies which ultimately concluded U.S. LNG exports show strong environmental benefits. The studies were conducted under both the Obama and Trump administrations.I firmly believe energy security is national security. That’s why the Biden administration’s decision to disrupt American LNG production is not only irresponsible to Americans, but also to our allies overseas. U.S. LNG exports have helped to wean European countries off Russian energy as the Russia-Ukraine war enters year three. Reversing this de facto ban means we can continue to export clean, affordable American natural gas to allies around the world long-term.Before serving in Congress, I spent my working life in the private sector. Like any business owner, I never made an investment unless I believed there would be a strong return. As natural gas producers and LNG exporters continue to review the president’s decision, they rightfully are concerned about their future. Why would you invest billions of dollars into a project without knowing if you are legally permitted to complete it? The International Energy Agency projects natural gas will play a major role in global energy consumption through 2050. The White House must reverse this decision if the U.S. is to remain a global LNG leader.The Biden administration’s political objectives coupled with the intense desire to implement green energy policies overnight are robbing Americans and our allies of a stable energy source as demand grows at home and abroad. Pennsylvania’s economic future, and the 423,000 jobs in the commonwealth that are supported by the natural gas industry, heavily depend on whether the Biden administration’s pause turns into an outright ban.Mike Kelly represents Pennsylvania’s 16th District. He is a member of the Ways & Means Committee and the House Natural Gas Caucus."
    ),

    "📰 EPA to delay rules for some power plants until after November": (
        "EPA to delay rules for some power plants until after November election The Environmental Protection Agency said Thursday it is delaying planned rules for existing natural gas plants that emit harmful air pollutants and contribute to global warming. "
        "FILE - Environmental Protection Agency Administrator Michael Regan waits for a speech by President Joe Biden about supply chain issues in the Indian Treaty Room on the White House complex in Washington,"
        " Nov. 27, 2023. The EPA said Feb. 29, 2024, it is delaying planned rules for existing natural gas plants that emit harmful air pollutants and contribute to global warming. "
        "(AP Photo/Andrew Harnik, File)WASHINGTON – The Environmental Protection Agency said Thursday it is delaying planned rules to curb emissions from existing natural gas plants that release harmful air pollutants and contribute to global warming."
        "The agency said it is still on track to finalize rules for coal-fired power plants and new gas plants that have not come online, a key step to slow planet-warming pollution from the power sector, the nation’s second-largest contributor to climate change."
        "Recommended VideosBut in a turnaround from previous plans, the agency said it will review standards for existing gas plants and expand the rules to include more pollutants. The change came after complaints from environmental justice groups, who said the earlier plan allowed too much toxic air pollution which disproportionately harms low-income neighborhoods near power plants, refineries and other industrial sites."
        "“As EPA works towards final standards to cut climate pollution from existing coal and new gas-fired power plants later this spring,"
        " the agency is taking a new, comprehensive approach to cover the entire fleet of natural gas-fired turbines, as well as cover more pollutants,'' EPA Administrator Michael Regan said in a statement.He called the new plan a “stronger, more durable approach” that will achieve greater emissions reductions than the current proposal. It also will better protect vulnerable frontline communities suffering from toxic air pollution caused by power plants and other industrial sites,"
        " Regan said.Still, the plan was not universally welcomed by environmentalists, who the said the new approach will likely push rules for existing gas plants past the November presidential election.“We are extremely disappointed in EPA’s decision to delay finalizing carbon pollution standards for existing gas plants, which make up a significant portion of carbon emissions in the power sector,'' said Frank Sturges, a lawyer for the Clean Air Task Force, an environmental group."
        "“Greenhouse gas emissions from power plants have gone uncontrolled for far too long, and we have no more time to waste,” he said.Other environmental groups hailed the decision, saying the new plan would ultimately deliver better results.“We have always known that the fight for a clean power sector wouldn’t be a quick one.,'' said Charles Harper of Evergreen Action."" ""EPA’s first order of business should be finalizing strong and necessary limits on climate pollution from new gas and existing coal plants as quickly as possible.''“We are glad that EPA is committed to finishing the job with a new rule that covers every gas plant operating in the U.S.,'' Harper added.“Tackling dirty coal plants is one of the single most important moves the president and EPA can make to rein in climate pollution,'' said Abigail Dillen, president of Earthjustice."
        "As utilities propose new fossil gas plants, we absolutely have to get ahead of a big new pollution problem.”EPA issued a proposed rule in May 2023 that called for drastically curbing greenhouse gas emissions from existing coal and gas-fired plants, as well as future gas plants planned by the power industry. No new coal plant has opened in the U.S. in more than a decade, while dozens of coal-fired plants have closed in recent years in the face of competition from cheaper natural gas. The Biden administration has committed to create a carbon pollution-free power sector by 2035."
        "The EPA proposal could force power plants to capture smokestack emissions using a technology that has long been promised but is not used widely in the United States.If finalized, the proposed regulation would mark the first time the federal government has restricted carbon dioxide emissions from existing power plants, which generate about 25% of U.S. greenhouse gas pollution, second only to the transportation sector. The rule also would apply to future electric plants and would avoid up to 617 million metric tons of carbon dioxide through 2042, equivalent to annual emissions of 137 million passenger vehicles, the EPA said.Almost all coal plants — along with large, frequently used gas-fired plants — would have to cut or capture nearly all their carbon dioxide emissions by 2038, the EPA said."
        " Plants that cannot meet the new standards would be forced to shutter.Much of the EPA plan is expected to be made final this spring and is likely to be challenged by industry groups and Republican-leaning states. They have accused the Democratic administration of overreach on environmental regulations and warn of a pending reliability crisis for the electric grid."
        " The power plant rule is one of at least a half-dozen EPA rules limiting power plant emissions and wastewater treatment.The National Mining Association warned of ""an onslaught” of government regulation “designed to shut down the coal fleet prematurely″ when the EPA proposal was announced last year.Regan has denied that the power plant rule is aimed at shutting down the coal sector, but acknowledged last year that, “ we will see some coal retirements.”Coal provides about 20% of U.S. electricity, down from about 45% in 2010. Natural gas provides about 40% of U.S. electricity."
        " The remainder comes from nuclear energy and renewables such as wind, solar and hydropower.Peggy Shepard,"
        " co-founder and executive director of WE ACT for Environmental Justice, a New York-based group, said she was pleased that the concerns of environmental justice communities will be factored into EPA's rulemaking."
        "“The power sector is one of the top sources of carbon emissions and pollution,'' she said. ""With this pause to take a deeper dive into developing the most comprehensive and thoughtful rulemaking for existing gas plants, "
        "we have an opportunity to do this work correctly and effectively to protect the human and environmental health of the most overburdened, neglected and vulnerable people across the country.'"
        "'The EPA's revised plan was first reported by Bloomberg News."

    )
}


# === Paste Mode ===
if input_mode == "📝 Paste Article":
    st.session_state.article_text = st.text_area(
        "Paste your article below:",
        value=st.session_state.article_text,
        height=150,
        placeholder="Paste the article text here..."
    )

# === Sample Mode ===
elif input_mode == "📚 Load Sample Article":
    sample_selected = st.selectbox("Select a sample article to load:", list(sample_articles.keys()))
    
    if st.button("📥 Load This Sample"):
        st.session_state.article_text = sample_articles[sample_selected]

    # Show the loaded article for editing
    st.session_state.article_text = st.text_area(
        "Loaded article (you can still edit it):",
        value=st.session_state.article_text,
        height=150
    )


# === Date Input ===
article_date = st.date_input("📅 Article Publish Date", value=date.today(), format="YYYY/MM/DD")

# === Prediction Button ===
if st.button("🔍 Predict Sentiment & Price"):
    if st.session_state.article_text and article_date:
        result = predict_sentiment_and_price(st.session_state.article_text, article_date)

        # === Sentiment Badge Styling ===
        def sentiment_box(sentiment):
            sentiment = sentiment.lower()
            styles = {
                "positive": "background-color:#d4edda; color:#155724; border:1px solid #c3e6cb;",
                "neutral": "background-color:#f8f9fa; color:#383d41; border:1px solid #d6d8db;",
                "negative": "background-color:#f8d7da; color:#721c24; border:1px solid #f5c6cb;"
            }
            style = styles.get(sentiment, "")
            return f"<span style='display:inline-block; padding:4px 10px; border-radius:5px; {style}'>{sentiment.capitalize()}</span>"

        # === Output Display ===
        st.markdown("---")
        st.subheader("🧠 Prediction Output")
        st.markdown(f"**Supply Sentiment:** {sentiment_box(result['supply_sentiment'])}", unsafe_allow_html=True)
        st.markdown(f"**Demand Sentiment:** {sentiment_box(result['demand_sentiment'])}", unsafe_allow_html=True)
        st.markdown(f"**Predicted Sentiment:** {sentiment_box(result['final_sentiment'])}", unsafe_allow_html=True)
        st.markdown(f"**Predicted Price:** <span style='font-weight:bold'>${result['predicted_price']:.2f}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='font-weight:bold'>Advice:</span> {result['advice']}", unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please enter both article text and publish date.")
