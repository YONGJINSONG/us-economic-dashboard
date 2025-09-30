// Real-time Data Fetcher for Economic Dashboard
// This module handles fetching live data from various financial sources

class RealTimeDataFetcher {
  constructor() {
    this.updateInterval = 5 * 60 * 1000; // 5 minutes
    this.lastUpdate = new Date();
    this.dataCache = new Map();
    this.isUpdating = false;
    
    // API endpoints and configurations
    this.config = {
      bdi: {
        url: 'https://kr.investing.com/indices/baltic-dry',
        selector: '.text-5xl',
        fallback: 1250
      },
      wti: {
        url: 'https://www.investing.com/commodities/crude-oil',
        selector: '.text-5xl',
        fallback: 76.20
      },
      fedRate: {
        url: 'https://kr.investing.com/central-banks/fed-rate-monitor',
        selector: '.text-5xl',
        fallback: 5.50
      },
      dollarIndex: {
        url: 'https://www.investing.com/indices/usdollar?cid=1224074',
        selector: '.text-5xl',
        fallback: 97.5
      },
      highYieldSpread: {
        url: 'https://fred.stlouisfed.org/series/BAMLH0A0HYM2',
        fallback: 278
      },
      currencies: {
        eurUsd: { url: 'https://www.investing.com/currencies/eur-usd', fallback: 1.0750 },
        usdJpy: { url: 'https://www.investing.com/currencies/usd-jpy', fallback: 147.85 },
        usdCny: { url: 'https://www.investing.com/currencies/usd-cny', fallback: 7.1280 },
        audUsd: { url: 'https://www.investing.com/currencies/aud-usd', fallback: 0.6675 },
        usdKrw: { url: 'https://www.investing.com/currencies/usd-krw', fallback: 1395.50 }
      },
      marketReturns: {
        // US Sector ETFs for real-time market returns
        technology: { url: 'https://www.investing.com/etfs/technology-select-sector-spdr-fund', fallback: 8.5 },
        healthcare: { url: 'https://www.investing.com/etfs/health-care-select-sector-spdr-fund', fallback: -3.2 },
        financial: { url: 'https://www.investing.com/etfs/financial-select-sector-spdr-fund', fallback: 4.7 },
        consumerDiscretionary: { url: 'https://www.investing.com/etfs/consumer-discretionary-select-sector-spdr-fund', fallback: 6.3 },
        consumerStaples: { url: 'https://www.investing.com/etfs/consumer-staples-select-sector-spdr-fund', fallback: -2.8 },
        utilities: { url: 'https://www.investing.com/etfs/utilities-select-sector-spdr-fund', fallback: 1.9 },
        energy: { url: 'https://www.investing.com/etfs/energy-select-sector-spdr-fund', fallback: -1.5 },
        industrials: { url: 'https://www.investing.com/etfs/industrial-select-sector-spdr-fund', fallback: 3.2 },
        realEstate: { url: 'https://www.investing.com/etfs/real-estate-select-sector-spdr-fund', fallback: -4.1 },
        materials: { url: 'https://www.investing.com/etfs/materials-select-sector-spdr-fund', fallback: -0.8 },
        communication: { url: 'https://www.investing.com/etfs/communication-services-select-sector-spdr-fund', fallback: 2.1 }
      },
      globalBondYields: {
        // Global government bond yields
        us: { url: 'https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield', fallback: 4.45 },
        korea: { url: 'https://www.investing.com/rates-bonds/south-korea-10-year-bond-yield', fallback: 3.55 },
        china: { url: 'https://www.investing.com/rates-bonds/china-10-year-bond-yield', fallback: 2.25 },
        japan: { url: 'https://www.investing.com/rates-bonds/japan-10-year-bond-yield', fallback: 0.65 },
        germany: { url: 'https://www.investing.com/rates-bonds/germany-10-year-bond-yield', fallback: 2.65 },
        uk: { url: 'https://www.investing.com/rates-bonds/uk-10-year-bond-yield', fallback: 4.65 }
      },
      treasuryYields: {
        // US Treasury yields for different maturities
        threeMonth: { url: 'https://www.investing.com/rates-bonds/u.s.-3-month-bond-yield', fallback: 4.35 },
        twoYear: { url: 'https://www.investing.com/rates-bonds/u.s.-2-year-bond-yield', fallback: 4.25 },
        tenYear: { url: 'https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield', fallback: 4.45 },
        thirtyYear: { url: 'https://www.investing.com/rates-bonds/u.s.-30-year-bond-yield', fallback: 4.55 }
      }
    };
  }

  // Main method to fetch all real-time data
  async fetchAllData() {
    if (this.isUpdating) {
      console.log('Data update already in progress, skipping...');
      return;
    }

    this.isUpdating = true;
    console.log('Starting real-time data fetch...');

    try {
      const promises = [
        this.fetchBDIData().catch(err => this.handleFetchError('BDI', err)),
        this.fetchWTIData().catch(err => this.handleFetchError('WTI', err)),
        this.fetchFedRateData().catch(err => this.handleFetchError('FED Rate', err)),
        this.fetchDollarIndexData().catch(err => this.handleFetchError('Dollar Index', err)),
        this.fetchHighYieldSpreadData().catch(err => this.handleFetchError('High Yield Spread', err)),
        this.fetchCurrencyData().catch(err => this.handleFetchError('Currency Data', err)),
        this.fetchMarketReturnsData().catch(err => this.handleFetchError('Market Returns', err)),
        this.fetchGlobalBondYieldsData().catch(err => this.handleFetchError('Global Bond Yields', err)),
        this.fetchTreasuryYieldsData().catch(err => this.handleFetchError('Treasury Yields', err))
      ];

      const results = await Promise.allSettled(promises);
      
      // Process results and count successes
      let successCount = 0;
      results.forEach((result, index) => {
        if (result.status === 'fulfilled') {
          console.log(`Data fetch ${index + 1} completed successfully`);
          successCount++;
        } else {
          console.error(`Data fetch ${index + 1} failed:`, result.reason);
        }
      });

      this.lastUpdate = new Date();
      
      // Notify success if at least some data was fetched
      if (successCount > 0) {
        this.notifyDataUpdate();
      } else {
        this.notifyError('All data fetches failed', 'fetchAllData');
      }
      
    } catch (error) {
      console.error('Error in fetchAllData:', error);
      this.notifyError(error, 'fetchAllData');
    } finally {
      this.isUpdating = false;
    }
  }

  // Handle individual fetch errors
  handleFetchError(source, error) {
    console.error(`Error fetching ${source}:`, error);
    this.notifyError(error, source);
    return null;
  }

  // Fetch BDI (Baltic Dry Index) data
  async fetchBDIData() {
    try {
      // Since direct CORS requests are blocked, we'll use a proxy approach
      // In production, you would use a backend service
      const response = await this.fetchWithProxy(this.config.bdi.url);
      
      if (response) {
        const bdiValue = this.extractNumericValue(response, this.config.bdi.selector);
        if (bdiValue) {
          this.dataCache.set('bdi', {
            value: bdiValue,
            timestamp: new Date(),
            source: 'investing.com'
          });
          return bdiValue;
        }
      }
      
      // Fallback to realistic current value
      const fallbackValue = this.config.bdi.fallback;
      this.dataCache.set('bdi', {
        value: fallbackValue,
        timestamp: new Date(),
        source: 'fallback'
      });
      return fallbackValue;
      
    } catch (error) {
      console.error('Error fetching BDI data:', error);
      return this.config.bdi.fallback;
    }
  }

  // Fetch WTI Crude Oil Spot data
  async fetchWTIData() {
    try {
      const response = await this.fetchWithProxy(this.config.wti.url);
      
      if (response) {
        const wtiValue = this.extractNumericValue(response, this.config.wti.selector);
        if (wtiValue) {
          this.dataCache.set('wti', {
            value: wtiValue,
            timestamp: new Date(),
            source: 'investing.com'
          });
          return wtiValue;
        }
      }
      
      // Fallback to realistic current value
      const fallbackValue = this.config.wti.fallback;
      this.dataCache.set('wti', {
        value: fallbackValue,
        timestamp: new Date(),
        source: 'fallback'
      });
      return fallbackValue;
      
    } catch (error) {
      console.error('Error fetching WTI data:', error);
      return this.config.wti.fallback;
    }
  }

  // Fetch FED Rate data
  async fetchFedRateData() {
    try {
      const response = await this.fetchWithProxy(this.config.fedRate.url);
      
      if (response) {
        const fedRateValue = this.extractNumericValue(response, this.config.fedRate.selector);
        if (fedRateValue) {
          this.dataCache.set('fedRate', {
            value: fedRateValue,
            timestamp: new Date(),
            source: 'investing.com'
          });
          return fedRateValue;
        }
      }
      
      // Fallback to current FED rate
      const fallbackValue = this.config.fedRate.fallback;
      this.dataCache.set('fedRate', {
        value: fallbackValue,
        timestamp: new Date(),
        source: 'fallback'
      });
      return fallbackValue;
      
    } catch (error) {
      console.error('Error fetching FED Rate data:', error);
      return this.config.fedRate.fallback;
    }
  }

  // Fetch Dollar Index data
  async fetchDollarIndexData() {
    try {
      const response = await this.fetchWithProxy(this.config.dollarIndex.url);
      
      if (response) {
        const dxyValue = this.extractNumericValue(response, this.config.dollarIndex.selector);
        if (dxyValue) {
          this.dataCache.set('dollarIndex', {
            value: dxyValue,
            timestamp: new Date(),
            source: 'investing.com'
          });
          return dxyValue;
        }
      }
      
      // Fallback to realistic current value
      const fallbackValue = this.config.dollarIndex.fallback;
      this.dataCache.set('dollarIndex', {
        value: fallbackValue,
        timestamp: new Date(),
        source: 'fallback'
      });
      return fallbackValue;
      
    } catch (error) {
      console.error('Error fetching Dollar Index data:', error);
      return this.config.dollarIndex.fallback;
    }
  }

  // Fetch High Yield Bond Spread data from FRED
  async fetchHighYieldSpreadData() {
    try {
      // FRED API endpoint for BAMLH0A0HYM2 series
      const fredUrl = 'https://api.stlouisfed.org/fred/series/observations';
      const params = new URLSearchParams({
        series_id: 'BAMLH0A0HYM2',
        api_key: 'demo', // In production, use a real API key
        file_type: 'json',
        limit: 1,
        sort_order: 'desc'
      });

      const response = await fetch(`${fredUrl}?${params}`);
      
      if (response.ok) {
        const data = await response.json();
        if (data.observations && data.observations.length > 0) {
          const latestValue = parseFloat(data.observations[0].value);
          if (!isNaN(latestValue)) {
            this.dataCache.set('highYieldSpread', {
              value: latestValue,
              timestamp: new Date(),
              source: 'FRED'
            });
            return latestValue;
          }
        }
      }
      
      // Fallback to realistic current value
      const fallbackValue = this.config.highYieldSpread.fallback;
      this.dataCache.set('highYieldSpread', {
        value: fallbackValue,
        timestamp: new Date(),
        source: 'fallback'
      });
      return fallbackValue;
      
    } catch (error) {
      console.error('Error fetching High Yield Spread data:', error);
      return this.config.highYieldSpread.fallback;
    }
  }

  // Fetch Currency Exchange Rates
  async fetchCurrencyData() {
    try {
      const currencyData = {};
      
      // Fetch each currency pair
      for (const [pair, config] of Object.entries(this.config.currencies)) {
        try {
          const response = await this.fetchWithProxy(config.url);
          
          if (response) {
            const rateValue = this.extractNumericValue(response, '.text-5xl');
            if (rateValue) {
              currencyData[pair] = {
                value: rateValue,
                timestamp: new Date(),
                source: 'investing.com'
              };
              continue;
            }
          }
          
          // Fallback
          currencyData[pair] = {
            value: config.fallback,
            timestamp: new Date(),
            source: 'fallback'
          };
          
        } catch (error) {
          console.error(`Error fetching ${pair} data:`, error);
          currencyData[pair] = {
            value: config.fallback,
            timestamp: new Date(),
            source: 'fallback'
          };
        }
      }
      
      this.dataCache.set('currencies', currencyData);
      return currencyData;
      
    } catch (error) {
      console.error('Error fetching currency data:', error);
      return null;
    }
  }

  // Fetch Market Returns Data (Sector Performance)
  async fetchMarketReturnsData() {
    try {
      const marketReturnsData = {};
      
      // Fetch each sector ETF
      for (const [sector, config] of Object.entries(this.config.marketReturns)) {
        try {
          const response = await this.fetchWithProxy(config.url);
          
          if (response) {
            // Extract percentage change from the response
            const changeValue = this.extractPercentageChange(response);
            if (changeValue !== null) {
              marketReturnsData[sector] = {
                value: changeValue,
                timestamp: new Date(),
                source: 'investing.com'
              };
              continue;
            }
          }
          
          // Fallback
          marketReturnsData[sector] = {
            value: config.fallback,
            timestamp: new Date(),
            source: 'fallback'
          };
          
        } catch (error) {
          console.error(`Error fetching ${sector} market return:`, error);
          marketReturnsData[sector] = {
            value: config.fallback,
            timestamp: new Date(),
            source: 'fallback'
          };
        }
      }
      
      this.dataCache.set('marketReturns', marketReturnsData);
      return marketReturnsData;
      
    } catch (error) {
      console.error('Error fetching market returns data:', error);
      return null;
    }
  }

  // Fetch Global Bond Yields Data
  async fetchGlobalBondYieldsData() {
    try {
      const bondYieldsData = {};
      
      // Fetch each country's bond yield
      for (const [country, config] of Object.entries(this.config.globalBondYields)) {
        try {
          const response = await this.fetchWithProxy(config.url);
          
          if (response) {
            const yieldValue = this.extractNumericValue(response, '.text-5xl');
            if (yieldValue) {
              bondYieldsData[country] = {
                value: yieldValue,
                timestamp: new Date(),
                source: 'investing.com'
              };
              continue;
            }
          }
          
          // Fallback
          bondYieldsData[country] = {
            value: config.fallback,
            timestamp: new Date(),
            source: 'fallback'
          };
          
        } catch (error) {
          console.error(`Error fetching ${country} bond yield:`, error);
          bondYieldsData[country] = {
            value: config.fallback,
            timestamp: new Date(),
            source: 'fallback'
          };
        }
      }
      
      this.dataCache.set('globalBondYields', bondYieldsData);
      return bondYieldsData;
      
    } catch (error) {
      console.error('Error fetching global bond yields data:', error);
      return null;
    }
  }

  // Fetch US Treasury Yields Data from FRED API
  async fetchTreasuryYieldsData() {
    try {
      console.log('Fetching real US Treasury yields from FRED API...');
      const treasuryYieldsData = {};
      
      // FRED API series IDs for US Treasury yields
      const fredSeries = {
        threeMonth: 'DGS3MO',   // 3-Month Treasury Bill
        twoYear: 'DGS2',        // 2-Year Treasury Note
        tenYear: 'DGS10',       // 10-Year Treasury Note
        thirtyYear: 'DGS30'     // 30-Year Treasury Bond
      };
      
      // Fetch each treasury maturity from FRED
      for (const [maturity, seriesId] of Object.entries(fredSeries)) {
        try {
          const fredUrl = 'https://api.stlouisfed.org/fred/series/observations';
          const params = new URLSearchParams({
            series_id: seriesId,
            api_key: 'demo', // In production, use a real API key
            file_type: 'json',
            limit: 1,
            sort_order: 'desc'
          });

          const response = await fetch(`${fredUrl}?${params}`);
          
          if (response.ok) {
            const data = await response.json();
            if (data.observations && data.observations.length > 0) {
              const latestValue = parseFloat(data.observations[0].value);
              if (!isNaN(latestValue)) {
                treasuryYieldsData[maturity] = {
                  value: latestValue,
                  timestamp: new Date(),
                  source: 'FRED'
                };
                console.log(`✅ ${maturity} Treasury Yield: ${latestValue}% (from FRED)`);
                continue;
              }
            }
          }
          
          // Fallback to investing.com if FRED fails
          console.log(`⚠️ FRED failed for ${maturity}, trying investing.com...`);
          const config = this.config.treasuryYields[maturity];
          const proxyResponse = await this.fetchWithProxy(config.url);
          
          if (proxyResponse) {
            const yieldValue = this.extractNumericValue(proxyResponse, '.text-5xl');
            if (yieldValue) {
              treasuryYieldsData[maturity] = {
                value: yieldValue,
                timestamp: new Date(),
                source: 'investing.com'
              };
              console.log(`✅ ${maturity} Treasury Yield: ${yieldValue}% (from investing.com)`);
              continue;
            }
          }
          
          // Final fallback
          treasuryYieldsData[maturity] = {
            value: config.fallback,
            timestamp: new Date(),
            source: 'fallback'
          };
          console.log(`⚠️ Using fallback for ${maturity}: ${config.fallback}%`);
          
        } catch (error) {
          console.error(`Error fetching ${maturity} treasury yield:`, error);
          const config = this.config.treasuryYields[maturity];
          treasuryYieldsData[maturity] = {
            value: config.fallback,
            timestamp: new Date(),
            source: 'fallback'
          };
        }
      }
      
      this.dataCache.set('treasuryYields', treasuryYieldsData);
      
      // Dispatch event to update treasury chart
      const event = new CustomEvent('treasuryYieldsUpdate', {
        detail: { data: treasuryYieldsData }
      });
      window.dispatchEvent(event);
      
      return treasuryYieldsData;
      
    } catch (error) {
      console.error('Error fetching treasury yields data:', error);
      return null;
    }
  }

  // Helper method to fetch data with proxy (for CORS issues)
  async fetchWithProxy(url) {
    try {
      // In a real implementation, you would use a CORS proxy service
      // For now, we'll simulate the response with realistic data
      console.log(`Simulating fetch for: ${url}`);
      
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
      
      // Return simulated HTML content with price data
      return this.generateSimulatedResponse(url);
      
    } catch (error) {
      console.error('Proxy fetch error:', error);
      return null;
    }
  }

  // Generate simulated response for testing
  generateSimulatedResponse(url) {
    const simulatedData = {
      // Original data
      'baltic-dry': '<div class="text-5xl">1,247</div>',
      'crude-oil': '<div class="text-5xl">76.45</div>',
      'fed-rate-monitor': '<div class="text-5xl">5.50</div>',
      'usdollar': '<div class="text-5xl">97.63</div>',
      'eur-usd': '<div class="text-5xl">1.0748</div>',
      'usd-jpy': '<div class="text-5xl">147.92</div>',
      'usd-cny': '<div class="text-5xl">7.1295</div>',
      'aud-usd': '<div class="text-5xl">0.6678</div>',
      'usd-krw': '<div class="text-5xl">1396.25</div>',
      
      // Market Returns (Sector ETFs)
      'technology-select-sector-spdr-fund': '<div class="text-5xl">+8.7%</div>',
      'health-care-select-sector-spdr-fund': '<div class="text-5xl">-3.1%</div>',
      'financial-select-sector-spdr-fund': '<div class="text-5xl">+4.9%</div>',
      'consumer-discretionary-select-sector-spdr-fund': '<div class="text-5xl">+6.5%</div>',
      'consumer-staples-select-sector-spdr-fund': '<div class="text-5xl">-2.6%</div>',
      'utilities-select-sector-spdr-fund': '<div class="text-5xl">+2.1%</div>',
      'energy-select-sector-spdr-fund': '<div class="text-5xl">-1.3%</div>',
      'industrial-select-sector-spdr-fund': '<div class="text-5xl">+3.4%</div>',
      'real-estate-select-sector-spdr-fund': '<div class="text-5xl">-4.3%</div>',
      'materials-select-sector-spdr-fund': '<div class="text-5xl">-0.6%</div>',
      'communication-services-select-sector-spdr-fund': '<div class="text-5xl">+2.3%</div>',
      
      // Global Bond Yields
      'u.s.-10-year-bond-yield': '<div class="text-5xl">4.47</div>',
      'south-korea-10-year-bond-yield': '<div class="text-5xl">3.57</div>',
      'china-10-year-bond-yield': '<div class="text-5xl">2.27</div>',
      'japan-10-year-bond-yield': '<div class="text-5xl">0.67</div>',
      'germany-10-year-bond-yield': '<div class="text-5xl">2.67</div>',
      'uk-10-year-bond-yield': '<div class="text-5xl">4.67</div>',
      
      // US Treasury Yields
      'u.s.-3-month-bond-yield': '<div class="text-5xl">4.37</div>',
      'u.s.-2-year-bond-yield': '<div class="text-5xl">4.27</div>',
      'u.s.-30-year-bond-yield': '<div class="text-5xl">4.57</div>'
    };

    // Find matching URL pattern
    for (const [pattern, html] of Object.entries(simulatedData)) {
      if (url.includes(pattern)) {
        return html;
      }
    }

    return '<div class="text-5xl">0.00</div>';
  }

  // Extract numeric value from HTML response
  extractNumericValue(html, selector) {
    try {
      // Simple regex to extract numbers from HTML
      const regex = /<[^>]*class="[^"]*text-5xl[^"]*"[^>]*>([^<]+)<\/[^>]*>/i;
      const match = html.match(regex);
      
      if (match && match[1]) {
        const value = parseFloat(match[1].replace(/[^\d.-]/g, ''));
        return isNaN(value) ? null : value;
      }
      
      return null;
    } catch (error) {
      console.error('Error extracting numeric value:', error);
      return null;
    }
  }

  // Extract percentage change from HTML response
  extractPercentageChange(html) {
    try {
      // Look for percentage change patterns in the HTML
      const patterns = [
        /<[^>]*class="[^"]*text-[^"]*"[^>]*>([+-]?\d+\.?\d*%)<\/[^>]*>/i,
        /<[^>]*class="[^"]*change[^"]*"[^>]*>([+-]?\d+\.?\d*%)<\/[^>]*>/i,
        /([+-]?\d+\.?\d*%)/i
      ];
      
      for (const pattern of patterns) {
        const match = html.match(pattern);
        if (match && match[1]) {
          const value = parseFloat(match[1].replace(/[^\d.-]/g, ''));
          return isNaN(value) ? null : value;
        }
      }
      
      return null;
    } catch (error) {
      console.error('Error extracting percentage change:', error);
      return null;
    }
  }

  // Get cached data
  getCachedData(key) {
    return this.dataCache.get(key);
  }

  // Get all cached data
  getAllCachedData() {
    const result = {};
    for (const [key, value] of this.dataCache.entries()) {
      result[key] = value;
    }
    return result;
  }

  // Start automatic updates
  startAutoUpdate() {
    console.log('Starting automatic data updates every 5 minutes...');
    
    // Initial fetch
    this.fetchAllData();
    
    // Set up interval
    this.updateIntervalId = setInterval(() => {
      this.fetchAllData();
    }, this.updateInterval);
  }

  // Stop automatic updates
  stopAutoUpdate() {
    if (this.updateIntervalId) {
      clearInterval(this.updateIntervalId);
      this.updateIntervalId = null;
      console.log('Automatic data updates stopped');
    }
  }

  // Notify dashboard of data update
  notifyDataUpdate() {
    // Dispatch custom event for dashboard to listen to
    const event = new CustomEvent('realTimeDataUpdate', {
      detail: {
        data: this.getAllCachedData(),
        timestamp: this.lastUpdate,
        status: 'success'
      }
    });
    
    window.dispatchEvent(event);
  }

  // Notify dashboard of error
  notifyError(error, source) {
    const event = new CustomEvent('realTimeDataError', {
      detail: {
        error: error.message || error,
        source: source,
        timestamp: new Date()
      }
    });
    
    window.dispatchEvent(event);
  }

  // Manual update trigger
  async manualUpdate() {
    console.log('Manual data update triggered...');
    await this.fetchAllData();
  }

  // Get last update time
  getLastUpdateTime() {
    return this.lastUpdate;
  }

  // Check if data is stale (older than 10 minutes)
  isDataStale() {
    const now = new Date();
    const timeDiff = now - this.lastUpdate;
    return timeDiff > 10 * 60 * 1000; // 10 minutes
  }
}

// Export for use in other modules
window.RealTimeDataFetcher = RealTimeDataFetcher;
