#!/usr/bin/python3
import asyncio
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from deepagents import create_deep_agent

# load envionment variables
load_dotenv()

# Make sure OPENAI_API_KEY is set in your environment
llm = ChatOpenAI(
    model="gpt-5-nano",
    openai_api_key=os.getenv("GPT_5")
)

# System Propmt to steer the agent to be an expert researcher
research_instruction="""You are an expert Trade researcher. Your job
is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `internet_search`

Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
"""

# build the agent
async def build_agent(client: MultiServerMCPClient):
    # load tools from all connected MCP servers
    # is async because MCP communication happens over I/O
    tools=await client.get_tools()

    # display the tool loaded 
    print(f"Loaded {len(tools)} tools: {[t.name for t in tools]}")

    # build the agent with all MCP tools
    agent=create_deep_agent(
        model=llm,
        tools=tools,
        system_prompt=research_instruction
    )

    return agent

async def main():
    # create one MC client connection to our local MCP
    # Transport here is stdio---> uses subprocess. Agent will run our program
    client=MultiServerMCPClient({
        "tools":{
            "command":"python",
            "args":["server.py"],
            "transport":"stdio",
        }
        # add here a remote mcp server ---> transport type "http"
    })

    # Build the agent after the MCP client is ready and tools are loaded
    agent=await build_agent(client)

    # pass a question
    question="what is the best strategy to trade future pairs XAU-USD?"

    # when in asynchronous mode use ainvoke not "invoke"
    result=await agent.ainvoke({"messages":[{"role":"user", "content":question}]})

    print(f"USER: {question}")
    # dislay the agent's response
    print(f"\nAI: {result['messages'][-1].content}\n")


if __name__=="__main__":
    asyncio.run(main())




"""
>python main.py
Loaded 1 tools: ['internet_search']
USER: what is the best strategy to trade future pairs XAU-USD?

AI: Short answer: there isn’t a single “best” strategy for XAU-USD futures. A robust approach is regime-aware trading that blends trend-following for the big moves with a carry/roll strategy to exploit the futures curve, plus disciplined intraday timing and strict risk controls. Below is a practical framework you can start with, plus the key context that matters for gold.

What to focus on (core ideas)
- Gold moves drop and reverse with macro regime shifts: USD strength (DXY), real yields, and risk sentiment matter as much as technicals.
- The futures curve can be exploited: contango or backwardation creates roll yield opportunities that can complement directional bets.
- Timeframe matters: use a multi-layer approach (daily/weekly for swing trades, and shorter intraday windows for timing) rather than a single horizon.

Three-pronged strategy you can implement
1) Core swing/trend strategy on GC near-month futures (daily/weekly timeframes)
- Purpose: capture the big, persistent moves in gold.
- Instrument: COMEX Gold futures (GC near-month). If you have smaller capital, consider micro GC (YG) to control risk.
- Entry rules (example, rules you can test and adapt):
  - Price closes above a rising 20-day EMA with ADX > 25 and a bullish MACD crossover, then enter long.
  - Or break above a defined resistance zone with increased volume.
  - For shorts, price closes below a falling 20-day EMA with ADX > 25 and bearish MACD crossover.
- Risk management:
  - Stop loss: ATR-based, e.g., 1.5x to 2x the current 14-day ATR from entry.
  - Position sizing: risk 0.5%–1% of account equity per trade; adjust for volatility and your liquidity.
  - Profit target / trail: use a fixed multiple (e.g., 2x risk) or a trailing stop that follows a moving average or ATR.
- Roll management:
  - Plan rolls near contract expiry to avoid excessive roll costs; monitor the curve as you roll.
- Why this works: you ride the dominant trend when momentum and volatility align; you’re protected by a disciplined exit if the regime changes.

2) Intraday/short-term timing overlay (1–15 minute charts)
- Purpose: improve entry timing and capture shorter moves, especially during high liquidity windows.
- Time windows: focus on London/New York overlap and key data releases; typical intraday moves in gold can be sizable.
- Entry rules (simplified):
  - Break of a defined intraday range with an above-average volume spike.
  - Use a tight intraday moving-average filter (e.g., price above/below a 5- or 15-period EMA on a 5-minute chart) combined with a momentum indicator (RSI or MACD).
- Risk management:
  - Very tight stops (e.g., 0.5x–1x ATR on the short horizon) and smaller position sizes.
  - Avoid chasing during illiquid periods or around major news releases when spreads widen.
- How this complements the core strategy: adds precise timing to enter the swing trades and can provide quick profits in trending sessions without waiting for a daily close.

3) Calendar spreads and carry/trend on the futures curve
- Purpose: capture roll yield and structural edge from the shape of the futures curve (contango vs backwardation).
- How to set it up:
  - Near-month long and far-month short (or vice versa) depending on the curve and your view of the curve’s evolution.
  - Trade when the curve is in a clear state (e.g., prolonged contango suggesting roll yield in a long near-month/short far-month setup, or backwardation suggesting the opposite).
- Risk considerations:
  - Curve dynamics can persist or flip; manage with daily P&L checks and have a plan to unwind if the curve steepens/sharpens beyond your risk tolerance.
  - Liquidity in calendar spreads is usually good but narrower than outright futures, so use appropriate order types and avoid excessive leverage.
- Why this matters: even if price direction is unclear, you can often earn from the curve movement and roll yield, providing diversification to your directional bets.

Key contextual factors to watch
- USD and rates: XAU-USD often moves inversely with the U.S. dollar and is sensitive to real yields. A weakening dollar or falling real yields can support gold prices.
- Market regime: in high-volatility risk-off periods, gold can rally as a safe haven; in strong risk-on environments, gold can lag stocks.
- Data cadence: major macro data (CPI, unemployment, Fed policy, FOMC statements) and central bank commentary can cause rapid regime shifts. Have a plan for these events (avoid over-leveraging, use wider stops, or reduce exposure).

Risk management fundamentals
- Don’t over-leverage: many gold strategies look attractive in backtests but fail in live trading if leverage is too high.
- Use ATR-based stops and target levels; keep risk per trade in a narrow band (0.5%–1% of equity is common for a start).
- Maintain a trading journal: track entry reasons, exit outcomes, and whether you adhered to risk controls. Review and refine weekly.
- Account for slippage and spreads: gold futures can have wide spreads during Asia-hours or around data releases; use limit orders where appropriate.

A practical 30-day starter plan
- Week 1: set up your tools
  - Chart GC near-month with 20/50/200 EMAs, RSI, MACD, ADX.
  - Build a daily routine to watch DXY, US 10-year yield, and the economic calendar.
  - Practice two rules-based entry ideas on paper or in a small live environment: (a) daily breakout/monthly trend entry, (b) intraday breakout entry.
- Week 2–3: small-scale live trading
  - Trade with strict risk controls (0.5%–1% risk per trade, 1–2 ATR stop on your chosen timeframes).
  - Start with the core swing strategy on GC near-month; add one intraday trade per day if your first trades are behaving well.
  - Begin exploring calendar spreads conceptually; do paper trades to understand curve behavior.
- Week 4: refine and build a simple plan
  - Decide which component delivers the best risk-adjusted results for you (swing vs intraday vs calendar spreads).
  - Begin implementing the chosen framework with a disciplined plan, larger but still controlled exposure, and a clear roll schedule.

What I can customize for you
- Timeframe and capital: Are you aiming for intraday scalping, short swings (days to weeks), or longer-term positions? How much capital do you have, and what level of risk per trade feels comfortable?
- Instrument preferences: Do you want to trade GC futures on a futures broker, micro GC for smaller risk, or incorporate XAUUSD spot as a complementary view?
- Risk tolerance and rules: Would you prefer a stricter stop-mechanism (e.g., guaranteed stops if available) or a looser, but more flexible, approach with a trailing stop?

If you’d like, I can turn this into a concrete, rule-based trading plan with exact entry/exit criteria, position sizing formulas, and a sample calendar spread setup you can test in a simulator. Share your timeframe, capital, and risk tolerance, and tell me whether you want purely futures-focused or a blended XAU-USD view.

"""