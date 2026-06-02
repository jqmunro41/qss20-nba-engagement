import "./App.css";

import topPlayerLift from "./assets/fig1_top_player_viewership_lift.png";
import playedVsMissed from "./assets/fig3_played_vs_missed_viewership.png";
import randomForestLift from "./assets/prediction_lift_by_player.png";
import headerStars from "./assets/qss20_website_header.png";

function App() {
  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">Jackson Munro: QSS20 Final Project</p>

    <img
        className="hero-image"
        src={headerStars}
        alt="NBA star players header graphic"/>

        <h1>Do NBA Stars Drive National TV Viewership?</h1>

        <p className="subtitle">
          This project analyzes 2023–24 NBA national TV regular-season games to
          examine whether star player availability and star matchups help
          explain national TV viewership.
        </p>
      </section>

      <section className="card">
        <h2>Research Question</h2>
        <p>
          The main question is whether specific NBA stars are associated with
          higher national TV viewership. 
        </p>
      </section>

      <section className="card">
        <h2>Data</h2>
        <p>
          The dataset includes 195 2023–24 NBA national TV regular-season games.
          The outcome is viewership in thousands. I added player availability
          indicators for All-Star players from that season and included game-level controls such
          as average net rating, spread, holiday status, closing total, and team
          valuation where relevant.
        </p>
      </section>

      <section className="card">
        <h2>Methods</h2>
        <p>
          I use three approaches: descriptive played-versus-not-played
          comparisons, OLS regressions with game-level controls, and a random
          forest model to estimate which players improve prediction of
          viewership.
        </p>
      </section>

      <section className="card">
  <h2>Result 1: Player Viewership Differences</h2>

  <figure className="figure-block">
    <img
      src={topPlayerLift}
      alt="Players associated with the largest national viewership increase"
    />
    <figcaption>
      This figure ranks players by the average viewership increase when they
      played. Stephen Curry shows the largest descriptive increase, followed by
      Jaylen Brown, Nikola Jokic, Jayson Tatum, and LeBron James.
    </figcaption>
  </figure>

  <figure className="figure-block">
    <img
      src={playedVsMissed}
      alt="Average viewership when selected stars played versus missed"
    />
    <figcaption>
      This figure compares average viewership of games for their own teams when selected stars played versus
      when they missed games. The orange points show average viewership of their teams when the
      player played, while the blue points show average viewership of their teams when the
      player missed.
    </figcaption>
  </figure>

  <p>
    Overall, the descriptive comparisons show that some stars are associated
    with higher average viewership. However, these raw differences should not be
    interpreted causally because national TV games are not randomly scheduled.
  </p>
</section>

      <section className="card">
  <h2>Result 2: Regression Results</h2>

  <div className="table-block">
    <h3>Player-Specific Regressions</h3>
    <table>
      <thead>
        <tr>
          <th>Player</th>
          <th>Games</th>
          <th>Coef.</th>
          <th>Effect</th>
          <th>p</th>
          <th>R²</th>
          <th>N</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>S. Curry</td><td>25</td><td>0.585</td><td>79.5%</td><td>0.000</td><td>0.157</td><td>195</td></tr>
        <tr><td>L. James</td><td>23</td><td>0.308</td><td>36.1%</td><td>0.100</td><td>0.109</td><td>195</td></tr>
        <tr><td>A. Davis</td><td>28</td><td>0.273</td><td>31.4%</td><td>0.087</td><td>0.108</td><td>195</td></tr>
        <tr><td>N. Jokic</td><td>22</td><td>0.270</td><td>31.0%</td><td>0.082</td><td>0.106</td><td>195</td></tr>
        <tr><td>J. Brown</td><td>27</td><td>0.229</td><td>25.7%</td><td>0.207</td><td>0.100</td><td>195</td></tr>
        <tr><td>J. Tatum</td><td>29</td><td>0.146</td><td>15.7%</td><td>0.445</td><td>0.096</td><td>195</td></tr>
        <tr><td>J. Brunson</td><td>14</td><td>0.134</td><td>14.4%</td><td>0.664</td><td>0.096</td><td>195</td></tr>
        <tr><td>B. Adebayo</td><td>15</td><td>0.122</td><td>13.0%</td><td>0.520</td><td>0.095</td><td>195</td></tr>
        <tr><td>T. Maxey</td><td>19</td><td>0.101</td><td>10.6%</td><td>0.539</td><td>0.095</td><td>195</td></tr>
        <tr><td>L. Doncic</td><td>15</td><td>0.095</td><td>10.0%</td><td>0.623</td><td>0.095</td><td>195</td></tr>
        <tr><td>D. Lillard</td><td>21</td><td>0.054</td><td>5.6%</td><td>0.799</td><td>0.094</td><td>195</td></tr>
        <tr><td>J. Randle</td><td>10</td><td>0.044</td><td>4.4%</td><td>0.912</td><td>0.094</td><td>195</td></tr>
        <tr><td>G. Antetokounmpo</td><td>20</td><td>-0.024</td><td>-2.4%</td><td>0.915</td><td>0.094</td><td>195</td></tr>
        <tr><td>K. Durant</td><td>25</td><td>-0.088</td><td>-8.4%</td><td>0.598</td><td>0.095</td><td>195</td></tr>
        <tr><td>K. Leonard</td><td>19</td><td>-0.097</td><td>-9.2%</td><td>0.574</td><td>0.095</td><td>195</td></tr>
        <tr><td>A. Edwards</td><td>12</td><td>-0.111</td><td>-10.5%</td><td>0.640</td><td>0.095</td><td>195</td></tr>
        <tr><td>P. George</td><td>20</td><td>-0.119</td><td>-11.2%</td><td>0.473</td><td>0.096</td><td>195</td></tr>
        <tr><td>D. Booker</td><td>21</td><td>-0.235</td><td>-20.9%</td><td>0.178</td><td>0.103</td><td>195</td></tr>
        <tr><td>S. Gilgeous-Alexander</td><td>11</td><td>-0.327</td><td>-27.9%</td><td>0.146</td><td>0.103</td><td>195</td></tr>
      </tbody>
    </table>
  </div>

  <div className="table-block">
    <h3>Opposing Star Matchup Regressions</h3>
    <table>
      <thead>
        <tr>
          <th>Matchup</th>
          <th>Games</th>
          <th>Coef.</th>
          <th>Effect</th>
          <th>p</th>
          <th>R²</th>
          <th>N</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>N. Jokic vs. P. George</td><td>3</td><td>0.519</td><td>68.0%</td><td>0.000</td><td>0.216</td><td>195</td></tr>
        <tr><td>K. Durant vs. L. Doncic</td><td>3</td><td>0.474</td><td>60.7%</td><td>0.010</td><td>0.215</td><td>195</td></tr>
        <tr><td>L. Doncic vs. D. Booker</td><td>3</td><td>0.474</td><td>60.7%</td><td>0.010</td><td>0.215</td><td>195</td></tr>
        <tr><td>N. Jokic vs. S. Curry</td><td>4</td><td>0.453</td><td>57.4%</td><td>0.000</td><td>0.216</td><td>195</td></tr>
        <tr><td>D. Lillard vs. J. Brown</td><td>4</td><td>0.403</td><td>49.6%</td><td>0.056</td><td>0.214</td><td>195</td></tr>
        <tr><td>J. Tatum vs. D. Lillard</td><td>4</td><td>0.403</td><td>49.6%</td><td>0.056</td><td>0.214</td><td>195</td></tr>
        <tr><td>G. Antetokounmpo vs. J. Brown</td><td>3</td><td>0.346</td><td>41.4%</td><td>0.227</td><td>0.210</td><td>195</td></tr>
        <tr><td>G. Antetokounmpo vs. J. Tatum</td><td>3</td><td>0.346</td><td>41.4%</td><td>0.227</td><td>0.210</td><td>195</td></tr>
        <tr><td>K. Durant vs. N. Jokic</td><td>3</td><td>0.310</td><td>36.3%</td><td>0.448</td><td>0.209</td><td>195</td></tr>
        <tr><td>D. Lillard vs. J. Brunson</td><td>3</td><td>-0.850</td><td>-57.3%</td><td>0.428</td><td>0.208</td><td>195</td></tr>
        <tr><td>G. Antetokounmpo vs. J. Brunson</td><td>3</td><td>-0.850</td><td>-57.3%</td><td>0.428</td><td>0.208</td><td>195</td></tr>
        <tr><td>J. Brown vs. J. Randle</td><td>3</td><td>-0.972</td><td>-62.2%</td><td>0.147</td><td>0.211</td><td>195</td></tr>
      </tbody>
    </table>
  </div>

  <p>
    The player-specific regressions suggest that Stephen Curry has the largest
    estimated association with national TV viewership after controls, while most
    other individual player estimates are not statistically significant. However, Jokic, LeBron, and Anthony Davis are significant at the 
    10% level. The matchup regressions show larger estimated effects for some star pairings,
    especially Jokic-Curry and Durant-Doncic type matchups, but these results
    should be interpreted cautiously because many matchup estimates are based on
    only three or four games.
  </p>
</section>

      <section className="card">
  <h2>Result 3: Random Forest Prediction Lift</h2>

  <figure className="figure-block">
    <img
      src={randomForestLift}
      alt="Predicted viewership lift by player from the random forest model"
    />
    <figcaption>
      This figure shows the predicted viewership lift associated with each
      player in the random forest model. Stephen Curry produces the largest
      positive prediction lift, followed by Jaylen Brown, Jayson Tatum, Nikola
      Jokic, and LeBron James.
    </figcaption>
  </figure>

  <p>
    The random forest model highlights which players most improve prediction of
    national TV viewership. These results are best interpreted as predictive
    rather than causal, but they reinforce the descriptive finding that a small
    group of stars are especially tied to larger audiences.
  </p>
</section>

      <section className="takeaway">
        <h2>Main Takeaway</h2>
        <p>
          NBA stars clearly matter for fan interest, but this project finds that
          their effects are easier to see descriptively and predictively than
          causally. After accounting for game context and overall team populariy, individual star effects
          become harder to isolate. The only star showing consistently significant impact on viewership across all models
          was Stephen Curry, with players like Nikola Jokic and LeBron James following closely behind. 
        </p>
      </section>
    </main>
  );
}

export default App;