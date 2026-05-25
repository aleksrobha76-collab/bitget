const POPULAR_MARKETS = [
  { symbol: 'BTCUSDT', label: 'BTC/USDT', name: 'Bitcoin' },
  { symbol: 'ETHUSDT', label: 'ETH/USDT', name: 'Ethereum' },
  { symbol: 'SOLUSDT', label: 'SOL/USDT', name: 'Solana' },
];

const DEFAULT_MARKET_SYMBOL = POPULAR_MARKETS[0].symbol;
const MARKET_STORAGE_KEY = 'cryptotrade:selectedSymbol';
const LANGUAGE_STORAGE_KEY = 'cryptotrade:language';
const DEFAULT_LANGUAGE = 'ru';
const LANGUAGE_LABELS = {
  ru: {
    documentLang: 'ru',
    locale: 'ru-RU',
    selectAria: 'Выбор языка',
    languageRussian: 'Русский',
    languageEnglish: 'English',
    homePremiumTrader: 'Премиум трейдер',
    balance: 'Баланс',
    pairMenuAria: 'Выбор торговой пары',
    timeLeft: 'Осталось',
    growth: 'РОСТ',
    fall: 'ПАДЕНИЕ',
    analytics: 'Аналитика',
    thirtyDayPl: '30Д P/L',
    portfolioStats: 'Статистика портфеля',
    realAnalytics: 'Реальная аналитика по вашим позициям',
    winrate: 'Винрейт',
    drawdown: 'Просадка',
    betHistory: 'История ставок',
    noBets: 'Нет ставок',
    totalBets: 'Всего ставок',
    wins: 'Побед',
    verifiedTrader: 'Верифицированный трейдер',
    capital: 'Капитал',
    accountProfile: 'Профиль аккаунта',
    personalData: 'Личные данные и статистика',
    betStats: 'Статистика ставок',
    betsShort: 'Ставок',
    winsShort: 'Победы',
    lossesShort: 'Пораж.',
    recentBets: 'Последние ставки',
    deposit: 'Пополнить',
    addFunds: 'Добавить средства',
    settingsTitle: 'Настройки',
    settingsSubtitle: 'Управление и параметры',
    paramsTitle: 'Параметры',
    paramsSubtitle: 'Уведомления, безопасность и интерфейс',
    appPanelTitle: 'Telegram Mini App',
    appPanelSubtitle: 'Авторизация через Telegram',
    symbol: 'Символ',
    language: 'Язык',
    adminPanel: 'Панель администратора',
    loadingAccess: 'Загрузка прав доступа...',
    players: 'Игроки',
    clients: 'Клиенты',
    bets: 'Ставки',
    myBets: 'Мои ставки',
    workers: 'Воркеры',
    loading: 'Загрузка...',
    support: 'Поддержка',
    account: 'Аккаунт',
    logout: 'Выйти',
    navMarket: 'РЫНОК',
    navStats: 'СТАТС',
    navProfile: 'ПРОФИЛЬ',
    navSettings: 'НАСТР',
    betAmount: 'Сумма ставки',
    customAmount: 'Другая сумма...',
    time: 'Время',
    oneMinute: '1 мин',
    fiveMinutes: '5 мин',
    fifteenMinutes: '15 мин',
    available: 'Доступно',
    selectedPair: 'Выбранная пара',
    cannotChangePair: symbol => `Нельзя менять пару, пока активна ставка по ${symbol}.`,
    chartUnavailable: 'График временно недоступен',
    trendEntry: 'ВХОД',
    trendTarget: 'ЦЕЛЬ',
    trendStop: 'СТОП',
    trendBet: 'СТАВКА',
    quotesPending: 'Ожидаем котировки',
    userFallback: 'Пользователь',
    placeBet: (amount, direction) => `Поставить ₽${amount} на ${direction}`,
    amountRequired: 'Введите сумму ставки',
    insufficientFunds: balance => `Недостаточно средств. Баланс: ₽${balance}`,
    betPlaceError: 'Ошибка при размещении ставки',
    entry: 'Вход',
    inGame: 'в игре',
    upSubtitle: 'Long +90%',
    downSubtitle: 'Short -100%',
    winMessage: payout => `Победа! +₽${payout}`,
    lossMessage: amount => `Поражение. -₽${amount}`,
    bestBet: (payout, symbol) => `Лучшая ставка: ₽${payout} на ${symbol}`,
    bestBetEmpty: 'Лучшая ставка: —',
    pending: 'В игре',
    win: 'Победа',
    loss: 'Поражение',
    adminOwnerTitle: 'Панель главного админа',
    adminWorkerTitle: 'Панель воркера',
    adminOwnerSubtitle: 'Игроки, ставки и контроль воркеров в одном месте.',
    adminWorkerSubtitle: (code, count) => `Ваш код: ${code} • Клиентов: ${count}`,
    loadPlayersError: 'не удалось загрузить игроков',
    loadBetsError: 'не удалось загрузить ставки',
    loadWorkersError: 'не удалось загрузить воркеров',
    error: 'Ошибка',
    referralTest: 'Тестовый код 0000',
    referralBy: (username, code) => `Привёл @${username} • код ${code}`,
    referralEmpty: 'Клиент без воркера',
    noPlayers: 'Нет игроков',
    noClientsList: 'Нет клиентов',
    outcomeSetting: 'Исход ставок',
    random: 'Рандом',
    balanceRub: 'Баланс (₽)',
    save: 'Сохранить',
    invalidPlayerId: 'Некорректный ID игрока',
    validAmount: 'Введите корректную сумму',
    balanceUpdated: amount => `Баланс обновлён: ₽${amount}`,
    player: 'Игрок',
    worker: 'Воркер',
    instrument: 'Инструмент',
    direction: 'Направление',
    stake: 'Ставка',
    status: 'Статус',
    date: 'Дата',
    test: 'тест',
    noWorkers: 'Нет воркеров',
    testCode: 'Тестовый код',
    betsCount: count => `${count} ставок`,
    noClients: 'Пока нет клиентов',
    codeClients: (code, count) => `Код ${code} • Клиентов ${count}`,
  },
  en: {
    documentLang: 'en',
    locale: 'en-US',
    selectAria: 'Language selection',
    languageRussian: 'Русский',
    languageEnglish: 'English',
    homePremiumTrader: 'Premium trader',
    balance: 'Balance',
    pairMenuAria: 'Trading pair selection',
    timeLeft: 'Time left',
    growth: 'UP',
    fall: 'DOWN',
    analytics: 'Analytics',
    thirtyDayPl: '30D P/L',
    portfolioStats: 'Portfolio statistics',
    realAnalytics: 'Real analytics for your positions',
    winrate: 'Win rate',
    drawdown: 'Drawdown',
    betHistory: 'Bet history',
    noBets: 'No bets',
    totalBets: 'Total bets',
    wins: 'Wins',
    verifiedTrader: 'Verified trader',
    capital: 'Capital',
    accountProfile: 'Account profile',
    personalData: 'Personal data and statistics',
    betStats: 'Bet statistics',
    betsShort: 'Bets',
    winsShort: 'Wins',
    lossesShort: 'Losses',
    recentBets: 'Recent bets',
    deposit: 'Deposit',
    addFunds: 'Add funds',
    settingsTitle: 'Settings',
    settingsSubtitle: 'Controls and preferences',
    paramsTitle: 'Preferences',
    paramsSubtitle: 'Notifications, security, and interface',
    appPanelTitle: 'Telegram Mini App',
    appPanelSubtitle: 'Telegram authorization',
    symbol: 'Symbol',
    language: 'Language',
    adminPanel: 'Admin panel',
    loadingAccess: 'Loading access...',
    players: 'Players',
    clients: 'Clients',
    bets: 'Bets',
    myBets: 'My bets',
    workers: 'Workers',
    loading: 'Loading...',
    support: 'Support',
    account: 'Account',
    logout: 'Log out',
    navMarket: 'MARKET',
    navStats: 'STATS',
    navProfile: 'PROFILE',
    navSettings: 'SETTINGS',
    betAmount: 'Bet amount',
    customAmount: 'Custom amount...',
    time: 'Time',
    oneMinute: '1 min',
    fiveMinutes: '5 min',
    fifteenMinutes: '15 min',
    available: 'Available',
    selectedPair: 'Selected pair',
    cannotChangePair: symbol => `You cannot change the pair while a ${symbol} bet is active.`,
    chartUnavailable: 'Chart is temporarily unavailable',
    trendEntry: 'ENTRY',
    trendTarget: 'TARGET',
    trendStop: 'STOP',
    trendBet: 'BET',
    quotesPending: 'Waiting for quotes',
    userFallback: 'User',
    placeBet: (amount, direction) => `Place ₽${amount} on ${direction}`,
    amountRequired: 'Enter the bet amount',
    insufficientFunds: balance => `Not enough funds. Balance: ₽${balance}`,
    betPlaceError: 'Failed to place bet',
    entry: 'Entry',
    inGame: 'in game',
    upSubtitle: 'Long +90%',
    downSubtitle: 'Short -100%',
    winMessage: payout => `Win! +₽${payout}`,
    lossMessage: amount => `Loss. -₽${amount}`,
    bestBet: (payout, symbol) => `Best bet: ₽${payout} on ${symbol}`,
    bestBetEmpty: 'Best bet: —',
    pending: 'In game',
    win: 'Win',
    loss: 'Loss',
    adminOwnerTitle: 'Main admin panel',
    adminWorkerTitle: 'Worker panel',
    adminOwnerSubtitle: 'Players, bets, and worker control in one place.',
    adminWorkerSubtitle: (code, count) => `Your code: ${code} • Clients: ${count}`,
    loadPlayersError: 'failed to load players',
    loadBetsError: 'failed to load bets',
    loadWorkersError: 'failed to load workers',
    error: 'Error',
    referralTest: 'Test code 0000',
    referralBy: (username, code) => `Referred by @${username} • code ${code}`,
    referralEmpty: 'Client without worker',
    noPlayers: 'No players',
    noClientsList: 'No clients',
    outcomeSetting: 'Bet outcome',
    random: 'Random',
    balanceRub: 'Balance (₽)',
    save: 'Save',
    invalidPlayerId: 'Invalid player ID',
    validAmount: 'Enter a valid amount',
    balanceUpdated: amount => `Balance updated: ₽${amount}`,
    player: 'Player',
    worker: 'Worker',
    instrument: 'Instrument',
    direction: 'Direction',
    stake: 'Bet',
    status: 'Status',
    date: 'Date',
    test: 'test',
    noWorkers: 'No workers',
    testCode: 'Test code',
    betsCount: count => `${count} bets`,
    noClients: 'No clients yet',
    codeClients: (code, count) => `Code ${code} • Clients ${count}`,
  },
};

const S = {
  tg: window.Telegram?.WebApp,
  initData: '',
  user: null,
  balance: 0,
  isAdmin: false,
  page: 'home',
  clock: { offsetMs: 0, syncedAt: 0 },
  chart: {
    candles: [],
    interval: '1m',
    price: 0,
    change: 0,
    high: 0,
    low: 0,
  },
  activeBet: null,
  bets: [],
  admin: {
    profile: null,
    users: [],
    bets: [],
    workers: [],
  },
  market: {
    options: POPULAR_MARKETS,
    selectedSymbol: DEFAULT_MARKET_SYMBOL,
    menuOpen: false,
  },
  language: DEFAULT_LANGUAGE,
  modal: {
    direction: 'up',
    keyboardOpen: false,
  },
};

async function requestJson(path, options = {}) {
  const response = await fetch(path, options);
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    let message = `${response.status} ${response.statusText}`;
    if (typeof data?.detail === 'string') message = data.detail;
    if (Array.isArray(data?.detail)) message = data.detail.map(item => item.msg || item.message || JSON.stringify(item)).join('; ');
    throw new Error(message);
  }
  return data;
}

async function api(method, path, body) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (S.initData) options.headers['X-Telegram-Init-Data'] = S.initData;
  if (body) options.body = JSON.stringify(body);

  const data = await requestJson(path, options);
  if (typeof data?.server_time === 'number') syncServerClock(data.server_time);
  return data;
}

function syncServerClock(serverTime) {
  if (!Number.isFinite(serverTime)) return;
  const nextOffset = serverTime * 1000 - Date.now();
  S.clock.offsetMs = S.clock.syncedAt ? (S.clock.offsetMs + nextOffset) / 2 : nextOffset;
  S.clock.syncedAt = Date.now();
}

function nowServerMs() {
  return Date.now() + S.clock.offsetMs;
}

function showMessage(message) {
  S.tg?.showAlert?.(message) || alert(message);
}

function getSavedMarketSymbol() {
  try {
    const saved = window.localStorage?.getItem(MARKET_STORAGE_KEY);
    return S.market.options.some(option => option.symbol === saved) ? saved : DEFAULT_MARKET_SYMBOL;
  } catch (_) {
    return DEFAULT_MARKET_SYMBOL;
  }
}

function saveMarketSymbol(symbol) {
  try {
    window.localStorage?.setItem(MARKET_STORAGE_KEY, symbol);
  } catch (_) {}
}

function getSavedLanguage() {
  try {
    const saved = window.localStorage?.getItem(LANGUAGE_STORAGE_KEY);
    return LANGUAGE_LABELS[saved] ? saved : DEFAULT_LANGUAGE;
  } catch (_) {
    return DEFAULT_LANGUAGE;
  }
}

function saveLanguage(language) {
  try {
    window.localStorage?.setItem(LANGUAGE_STORAGE_KEY, language);
  } catch (_) {}
}

function setText(id, value) {
  const node = el(id);
  if (node) node.textContent = value;
}

function t(key, ...args) {
  const labels = LANGUAGE_LABELS[S.language] || LANGUAGE_LABELS[DEFAULT_LANGUAGE];
  const fallback = LANGUAGE_LABELS[DEFAULT_LANGUAGE] || {};
  const value = labels[key] ?? fallback[key] ?? key;
  return typeof value === 'function' ? value(...args) : value;
}

function getLocale() {
  return t('locale');
}

function applyStaticTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(node => {
    node.textContent = t(node.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(node => {
    node.setAttribute('placeholder', t(node.dataset.i18nPlaceholder));
  });
  document.querySelectorAll('[data-i18n-aria-label]').forEach(node => {
    node.setAttribute('aria-label', t(node.dataset.i18nAriaLabel));
  });
}

function renderLanguageUI() {
  const labels = LANGUAGE_LABELS[S.language] || LANGUAGE_LABELS[DEFAULT_LANGUAGE];
  document.documentElement.lang = labels.documentLang;
  const select = el('language-select');
  if (select) {
    select.value = S.language;
    select.setAttribute('aria-label', labels.selectAria);
  }
  applyStaticTranslations();
  renderBetButtonLabels();
  renderPairUI();
  renderUserUI();
  updatePriceUI();
  updateConfirmButton();
  if (S.activeBet) showActiveBet();
  if (S.page === 'stats') renderStatsPage();
  if (S.page === 'profile') renderProfilePage();
  if (S.admin.profile) {
    renderAdminShell();
    if (S.admin.users.length) renderAdminUsers();
    if (S.admin.bets.length) renderAdminBets();
    if (S.admin.workers.length) renderAdminWorkers();
  }
}

function setLanguage(language) {
  if (!LANGUAGE_LABELS[language]) return;
  S.language = language;
  saveLanguage(language);
  renderLanguageUI();
}

function getMarketOption(symbol = S.market.selectedSymbol) {
  return S.market.options.find(option => option.symbol === symbol) || {
    symbol,
    label: fmtSymbol(symbol),
    name: t('selectedPair'),
  };
}

function getSelectedMarketLabel() {
  return getMarketOption().label;
}

function renderPairMenu() {
  const menu = el('pair-menu');
  if (!menu) return;

  menu.innerHTML = S.market.options.map(option => `
    <button
      class="pair-option ${option.symbol === S.market.selectedSymbol ? 'active' : ''}"
      type="button"
      data-symbol="${option.symbol}"
      role="option"
      aria-selected="${option.symbol === S.market.selectedSymbol ? 'true' : 'false'}"
    >
      <span class="pair-option-main">
        <span class="pair-option-symbol">${option.label}</span>
        <span class="pair-option-name">${option.name}</span>
      </span>
      <span class="pair-option-mark">${option.symbol.replace('USDT', '')}</span>
    </button>
  `).join('');

  menu.querySelectorAll('.pair-option').forEach(button => {
    button.addEventListener('click', () => selectMarket(button.dataset.symbol));
  });
}

function renderPairUI() {
  const option = getMarketOption();
  if (el('pair-chip-label')) el('pair-chip-label').textContent = option.label;
  if (el('set-symbol')) el('set-symbol').textContent = option.label;
  if (el('bm-symbol')) el('bm-symbol').textContent = option.label;
  el('pair-chip')?.classList.toggle('locked', Boolean(S.activeBet));
  renderPairMenu();
}

function openPairMenu() {
  if (S.activeBet) {
    showMessage(t('cannotChangePair', fmtSymbol(S.activeBet.symbol)));
    return;
  }
  S.market.menuOpen = true;
  el('pair-menu')?.classList.add('open');
  el('pair-chip')?.classList.add('open');
  el('pair-chip')?.setAttribute('aria-expanded', 'true');
}

function closePairMenu() {
  S.market.menuOpen = false;
  el('pair-menu')?.classList.remove('open');
  el('pair-chip')?.classList.remove('open');
  el('pair-chip')?.setAttribute('aria-expanded', 'false');
}

function togglePairMenu() {
  if (S.market.menuOpen) closePairMenu();
  else openPairMenu();
}

function selectMarket(symbol, options = {}) {
  const { persist = true, force = false, refresh = true } = options;
  if (!symbol) return;
  if (S.activeBet && !force && symbol !== S.market.selectedSymbol) {
    showMessage(t('cannotChangePair', fmtSymbol(S.activeBet.symbol)));
    return;
  }

  S.market.selectedSymbol = symbol;
  if (persist) saveMarketSymbol(symbol);
  renderPairUI();
  closePairMenu();
  updateTrendStrip();
  updateModalHeader();
  if (refresh) loadChart();
}

async function init() {
  if (S.tg) {
    S.tg.ready();
    S.tg.expand();
    S.tg.setHeaderColor?.('#050507');
    S.tg.setBackgroundColor?.('#050507');
    S.initData = S.tg.initData || '';
  }

  S.language = getSavedLanguage();
  renderLanguageUI();
  S.market.selectedSymbol = getSavedMarketSymbol();
  renderPairUI();

  try {
    const me = await api('GET', '/api/me');
    S.user = me;
    S.balance = me.balance ?? 0;
    S.activeBet = me.active_bet || null;
    if (S.activeBet?.symbol) {
      selectMarket(S.activeBet.symbol, { persist: false, force: true, refresh: false });
    }
    renderUserUI();
    if (S.activeBet) showActiveBet();
    else enableBetButtons();
  } catch (_) {
    enableBetButtons();
  }

  await loadAdminAccess();
  await Promise.all([loadChart(), loadBets()]);
  startPricePoll();

  el('loading-screen').classList.add('hidden');
  el('main-app').classList.remove('hidden');
}

document.querySelectorAll('.nav-tab').forEach(button => {
  button.addEventListener('click', () => switchPage(button.dataset.page));
});

el('pair-chip')?.addEventListener('click', event => {
  event.stopPropagation();
  togglePairMenu();
});

el('language-select')?.addEventListener('change', event => {
  setLanguage(event.target.value);
  S.tg?.HapticFeedback?.selectionChanged();
});

document.addEventListener('click', event => {
  const chip = el('pair-chip');
  const menu = el('pair-menu');
  if (!chip || !menu || !S.market.menuOpen) return;
  if (chip.contains(event.target) || menu.contains(event.target)) return;
  closePairMenu();
});

function switchPage(page) {
  closeBetModal();
  closePairMenu();
  document.querySelectorAll('.page').forEach(item => item.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(item => item.classList.remove('active'));
  el('page-' + page)?.classList.add('active');
  el('tab-' + page)?.classList.add('active');
  S.page = page;
  if (page === 'stats') renderStatsPage();
  if (page === 'profile') renderProfilePage();
  if (page === 'settings' && S.isAdmin) loadAdminData();
}

async function loadChart() {
  const loader = el('chart-loader');
  loader?.classList.remove('hidden');
  try {
    const symbol = S.market.selectedSymbol;
    const [candles, ticker] = await Promise.all([
      requestJson(`/api/klines/${symbol}?interval=${S.chart.interval}&limit=80`),
      requestJson(`/api/ticker24h/${symbol}`),
    ]);
    S.chart.candles = Array.isArray(candles) ? candles : [];
    S.chart.price = parseFloat(ticker.price) || 0;
    S.chart.change = parseFloat(ticker.change) || 0;
    S.chart.high = parseFloat(ticker.high) || 0;
    S.chart.low = parseFloat(ticker.low) || 0;
    updatePriceUI();
    drawChart();
  } catch (error) {
    console.warn('chart', error);
    if (!S.chart.candles.length) drawChartPlaceholder(t('chartUnavailable'));
  } finally {
    loader?.classList.add('hidden');
  }
}

function updatePriceUI() {
  const price = S.chart.price;
  const change = S.chart.change;
  if (el('sc-price')) el('sc-price').textContent = fmtPrice(price);
  if (el('sc-change')) {
    el('sc-change').textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`;
    el('sc-change').className = 'stat-card ' + (change >= 0 ? 'green' : 'red');
  }
  updateTrendStrip();
  updateModalHeader();
}

function updateTrendStrip() {
  if (!el('trend-text')) return;
  if (S.activeBet) {
    const bet = S.activeBet;
    el('trend-text').textContent = `${fmtSymbol(bet.symbol)}   ${formatDirection(bet.direction, true)}   ${t('trendEntry')} ${fmtPrice(bet.entry_price)}   ${t('trendBet')} ₽${bet.amount}`;
  } else if (S.chart.price) {
    el('trend-text').textContent = `${getSelectedMarketLabel()}   ${t('trendEntry')} ${fmtPrice(S.chart.price)}   ${t('trendTarget')} ${fmtPrice(S.chart.price * 1.005)}   ${t('trendStop')} ${fmtPrice(S.chart.price * 0.995)}`;
  } else {
    el('trend-text').textContent = `${t('trendEntry')} —   ${t('trendTarget')} —   ${t('trendStop')} —`;
  }

  const profitLoss = el('sc-pl');
  if (!profitLoss) return;
  if (S.activeBet && S.chart.price) {
    const diff = S.chart.price - S.activeBet.entry_price;
    const isWin = S.activeBet.direction === 'up' ? diff > 0 : diff < 0;
    profitLoss.textContent = 'P/L ' + (isWin ? '+₽' : '-₽') + (isWin ? (S.activeBet.amount * 0.9).toFixed(0) : S.activeBet.amount.toFixed(0));
    profitLoss.className = 'stat-card ' + (isWin ? 'green' : 'red');
  } else {
    profitLoss.textContent = 'P/L —';
    profitLoss.className = 'stat-card';
  }
}

function drawChart() {
  const canvas = el('chart-canvas');
  const wrap = el('chart-area');
  if (!canvas || !wrap) return;
  if (!S.chart.candles.length) {
    drawChartPlaceholder(t('quotesPending'));
    return;
  }

  const dpr = window.devicePixelRatio || 1;
  const width = wrap.clientWidth;
  const height = wrap.clientHeight;
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = width + 'px';
  canvas.style.height = height + 'px';

  const ctx = canvas.getContext('2d');
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.scale(dpr, dpr);

  ctx.fillStyle = '#111214';
  ctx.fillRect(0, 0, width, height);

  const candles = S.chart.candles.slice(-42);
  const paddingLeft = 44;
  const paddingRight = 18;
  const paddingTop = 10;
  const paddingBottom = 22;
  const chartWidth = width - paddingLeft - paddingRight;
  const chartHeight = height - paddingTop - paddingBottom;

  const maxPrice = Math.max(...candles.map(item => item.h));
  const minPrice = Math.min(...candles.map(item => item.l));
  const priceRange = Math.max(maxPrice - minPrice, 1);
  const step = chartWidth / Math.max(candles.length, 1);

  const yForPrice = price => paddingTop + chartHeight * (1 - (price - minPrice) / priceRange);

  ctx.strokeStyle = '#1c2030';
  ctx.lineWidth = 0.6;
  for (let index = 0; index <= 4; index += 1) {
    const y = paddingTop + chartHeight * (index / 4);
    ctx.beginPath();
    ctx.moveTo(paddingLeft, y);
    ctx.lineTo(width - paddingRight, y);
    ctx.stroke();
    const label = (maxPrice - (priceRange * index) / 4).toFixed(0);
    ctx.fillStyle = '#4a5568';
    ctx.font = '9px Inter, sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(label, paddingLeft - 4, y + 3);
  }

  candles.forEach((candle, index) => {
    const x = paddingLeft + step * index + step / 2;
    const isBull = candle.c >= candle.o;
    const color = isBull ? '#24F6A7' : '#FF5A6A';
    const bodyTop = yForPrice(Math.max(candle.c, candle.o));
    const bodyBottom = yForPrice(Math.min(candle.c, candle.o));
    const bodyHeight = Math.max(2, bodyBottom - bodyTop);
    const bodyWidth = Math.max(3, step * 0.58);

    ctx.strokeStyle = color;
    ctx.beginPath();
    ctx.moveTo(x, yForPrice(candle.h));
    ctx.lineTo(x, yForPrice(candle.l));
    ctx.stroke();

    ctx.fillStyle = color;
    ctx.fillRect(x - bodyWidth / 2, bodyTop, bodyWidth, bodyHeight);
  });

  if (S.chart.price) {
    const priceY = yForPrice(S.chart.price);
    ctx.setLineDash([4, 4]);
    ctx.strokeStyle = '#4DD5FF';
    ctx.beginPath();
    ctx.moveTo(paddingLeft, priceY);
    ctx.lineTo(width - paddingRight, priceY);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#4DD5FF';
    ctx.font = 'bold 10px Inter, sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(fmtPriceShort(S.chart.price), paddingLeft + 8, Math.max(14, priceY - 6));
  }

  if (S.activeBet?.entry_price) {
    const entryY = yForPrice(S.activeBet.entry_price);
    ctx.setLineDash([6, 5]);
    ctx.strokeStyle = S.activeBet.direction === 'up' ? '#24F6A7' : '#FF5A6A';
    ctx.beginPath();
    ctx.moveTo(paddingLeft, entryY);
    ctx.lineTo(width - paddingRight, entryY);
    ctx.stroke();
    ctx.setLineDash([]);
  }
}


function drawChartPlaceholder(message) {
  const canvas = el('chart-canvas');
  const wrap = el('chart-area');
  if (!canvas || !wrap) return;

  const dpr = window.devicePixelRatio || 1;
  const width = Math.max(wrap.clientWidth, 1);
  const height = Math.max(wrap.clientHeight, 1);
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = width + 'px';
  canvas.style.height = height + 'px';

  const ctx = canvas.getContext('2d');
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.scale(dpr, dpr);
  ctx.fillStyle = '#111214';
  ctx.fillRect(0, 0, width, height);
  ctx.strokeStyle = '#1c2030';
  ctx.lineWidth = 0.8;
  for (let index = 0; index < 5; index += 1) {
    const y = 16 + (height - 32) * (index / 4);
    ctx.beginPath();
    ctx.moveTo(18, y);
    ctx.lineTo(width - 18, y);
    ctx.stroke();
  }
  ctx.fillStyle = '#8FA2C1';
  ctx.font = '600 12px Inter, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(message, width / 2, height / 2);
}

document.querySelectorAll('.tf').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.tf').forEach(item => item.classList.remove('active'));
    button.classList.add('active');
    S.chart.interval = button.dataset.iv;
    if (el('set-interval')) el('set-interval').textContent = button.dataset.iv;
    loadChart();
  });
});

function startPricePoll() {
  clearInterval(window.__pricePollTimer);
  clearInterval(window.__chartReloadTimer);

  window.__pricePollTimer = setInterval(async () => {
    try {
      const ticker = await requestJson(`/api/ticker24h/${S.market.selectedSymbol}`);
      S.chart.price = parseFloat(ticker.price) || S.chart.price;
      S.chart.change = parseFloat(ticker.change) || 0;
      S.chart.high = parseFloat(ticker.high) || 0;
      S.chart.low = parseFloat(ticker.low) || 0;
      updatePriceUI();
      if (S.page === 'home') drawChart();
      updateActiveBetPL();
    } catch (error) {
      console.warn('ticker poll', error);
    }
  }, 3000);

  window.__chartReloadTimer = setInterval(() => {
    if (S.page === 'home') loadChart();
  }, 60000);
}

window.addEventListener('resize', () => {
  if (S.page === 'home') drawChart();
  syncModalViewport();
});

function renderUserUI() {
  if (!S.user) return;
  const username = S.user.username ? '@' + S.user.username : 'ID ' + (S.user.telegram_id || '');
  if (el('hc-name')) el('hc-name').textContent = username;
  if (el('stats-hc-name')) el('stats-hc-name').textContent = username;
  if (el('pr-name')) el('pr-name').textContent = username;
  if (el('pr-hero-name')) el('pr-hero-name').textContent = username;
  if (el('pr-hero-meta')) el('pr-hero-meta').textContent = 'UID ' + (S.user.telegram_id || '—');
  renderBalance();
}

function renderBalance() {
  if (el('hc-bal-val')) el('hc-bal-val').textContent = '₽' + rub(S.balance);
  if (el('pr-bal')) el('pr-bal').textContent = '₽' + rub(S.balance);
  if (el('pr-hero-bal')) el('pr-hero-bal').textContent = rub(S.balance);
  if (el('bm-balance')) el('bm-balance').textContent = '₽' + rub(S.balance);
}

el('open-up-btn')?.addEventListener('click', () => openBetModal('up'));
el('open-down-btn')?.addEventListener('click', () => openBetModal('down'));
el('bet-confirm-btn')?.addEventListener('click', () => placeBet(S.modal.direction));
el('bet-amount')?.addEventListener('input', () => {
  document.querySelectorAll('.bm-preset').forEach(button => button.classList.remove('active'));
  updateConfirmButton();
  syncModalViewport();
});

el('bet-amount')?.addEventListener('focus', () => {
  window.setTimeout(syncModalViewport, 40);
});

el('bet-amount')?.addEventListener('blur', () => {
  window.setTimeout(syncModalViewport, 120);
});

document.querySelectorAll('.bm-preset').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.bm-preset').forEach(item => item.classList.remove('active'));
    button.classList.add('active');
    if (el('bet-amount')) el('bet-amount').value = button.dataset.val;
    updateConfirmButton();
  });
});

document.querySelectorAll('.bm-dur').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.bm-dur').forEach(item => item.classList.remove('active'));
    button.classList.add('active');
  });
});

document.addEventListener('keydown', event => {
  if (event.key === 'Escape') closeBetModal();
});

window.visualViewport?.addEventListener('resize', syncModalViewport);
window.visualViewport?.addEventListener('scroll', syncModalViewport);

function openBetModal(direction) {
  if (S.activeBet) return;
  S.modal.direction = direction;
  const header = el('bm-dir-header');
  if (header) header.className = 'bm-dir-header ' + direction;
  if (el('bm-dir-arrow')) el('bm-dir-arrow').textContent = direction === 'up' ? '↑' : '↓';
  if (el('bm-dir-title')) el('bm-dir-title').textContent = formatDirection(direction);
  updateModalHeader();
  updateConfirmButton();
  el('bet-modal')?.classList.add('open');
  el('bet-modal')?.setAttribute('aria-hidden', 'false');
  el('modal-overlay')?.classList.add('show');
  el('modal-overlay')?.setAttribute('aria-hidden', 'false');
  syncModalViewport();
  window.setTimeout(() => {
    const amountInput = el('bet-amount');
    amountInput?.focus({ preventScroll: true });
    amountInput?.select?.();
    syncModalViewport();
  }, 80);
}

function closeBetModal() {
  el('bet-modal')?.classList.remove('open');
  el('bet-modal')?.setAttribute('aria-hidden', 'true');
  el('modal-overlay')?.classList.remove('show');
  el('modal-overlay')?.setAttribute('aria-hidden', 'true');
  S.modal.keyboardOpen = false;
  syncModalViewport();
}

function updateModalHeader() {
  const price = S.chart.price;
  const change = S.chart.change;
  if (el('bm-dir-title')) el('bm-dir-title').textContent = formatDirection(S.modal.direction);
  if (el('bm-symbol')) el('bm-symbol').textContent = getSelectedMarketLabel();
  if (el('bm-price')) el('bm-price').textContent = price ? fmtPrice(price) : '—';
  if (el('bm-change')) {
    el('bm-change').textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`;
    el('bm-change').className = 'bm-change-badge ' + (change > 0 ? 'up' : change < 0 ? 'down' : 'neutral');
  }
  if (el('bm-balance')) el('bm-balance').textContent = '₽' + rub(S.balance);
}

function updateConfirmButton() {
  const button = el('bet-confirm-btn');
  if (!button) return;
  const amount = parseFloat(el('bet-amount')?.value || '0') || 0;
  const direction = S.modal.direction;
  button.className = 'bm-confirm ' + direction;
  button.textContent = t('placeBet', amount, formatDirection(direction));
  button.disabled = amount <= 0 || !S.initData;
}

function syncModalViewport() {
  const modal = el('bet-modal');
  if (!modal) return;

  const rootStyle = document.documentElement.style;
  const viewport = window.visualViewport;
  const baseHeight = window.innerHeight || document.documentElement.clientHeight || 0;
  let keyboardOffset = 0;
  let viewportHeight = baseHeight;

  if (viewport) {
    viewportHeight = viewport.height;
    keyboardOffset = Math.max(0, baseHeight - (viewport.height + viewport.offsetTop));
  }

  S.modal.keyboardOpen = keyboardOffset > 120;
  modal.classList.toggle('keyboard-open', S.modal.keyboardOpen);
  rootStyle.setProperty('--bet-modal-bottom-offset', `${Math.max(0, keyboardOffset)}px`);
  rootStyle.setProperty('--bet-modal-max-height', `${Math.max(320, viewportHeight)}px`);

  if (S.modal.keyboardOpen) {
    const focused = document.activeElement;
    if (focused && modal.contains(focused)) {
      window.setTimeout(() => {
        focused.scrollIntoView({ block: 'center', behavior: 'smooth' });
      }, 60);
    }
  }
}

function enableBetButtons() {
  if (el('open-up-btn')) el('open-up-btn').disabled = false;
  if (el('open-down-btn')) el('open-down-btn').disabled = false;
  if (el('bet-confirm-btn')) el('bet-confirm-btn').disabled = false;
}

function disableBetButtons() {
  if (el('open-up-btn')) el('open-up-btn').disabled = true;
  if (el('open-down-btn')) el('open-down-btn').disabled = true;
  if (el('bet-confirm-btn')) el('bet-confirm-btn').disabled = true;
}

function renderBetButtonLabels() {
  if (S.activeBet) return;
  if (el('open-up-btn')?.querySelector('.ab-sub')) el('open-up-btn').querySelector('.ab-sub').textContent = t('upSubtitle');
  if (el('open-down-btn')?.querySelector('.ab-sub')) el('open-down-btn').querySelector('.ab-sub').textContent = t('downSubtitle');
}

async function placeBet(direction) {
  const amount = parseFloat(el('bet-amount')?.value || '0');
  const duration = parseInt(document.querySelector('.bm-dur.active')?.dataset.dur || '60', 10);
  if (!amount || amount <= 0) {
    showMessage(t('amountRequired'));
    return;
  }
  if (amount > S.balance) {
    showMessage(t('insufficientFunds', rub(S.balance)));
    return;
  }

  disableBetButtons();
  try {
    const result = await api('POST', '/api/bet', {
      direction,
      amount,
      symbol: S.market.selectedSymbol,
      duration,
    });
    S.activeBet = result.bet;
    S.balance = result.balance;
    if (S.activeBet?.symbol) selectMarket(S.activeBet.symbol, { persist: false, force: true, refresh: false });
    renderBalance();
    closeBetModal();
    showActiveBet();
    S.tg?.HapticFeedback?.impactOccurred('medium');
  } catch (error) {
    enableBetButtons();
    showMessage(error.message || t('betPlaceError'));
  }
}

function showActiveBet() {
  const bet = S.activeBet;
  if (!bet) return;
  disableBetButtons();
  el('active-bet-bar')?.classList.remove('hidden');
  renderPairUI();
  syncChartBetState();
  if (el('abb-dir-icon')) {
    el('abb-dir-icon').textContent = bet.direction === 'up' ? '↑' : '↓';
    el('abb-dir-icon').className = 'abb-dir ' + bet.direction;
  }
  if (el('abb-label')) el('abb-label').textContent = `${fmtSymbol(bet.symbol)} • ${formatDirection(bet.direction)} • ₽${bet.amount}`;
  if (el('abb-entry')) el('abb-entry').textContent = `${t('entry')}: ${fmtPrice(bet.entry_price)}`;
  if (el('open-up-btn')?.querySelector('.ab-sub')) el('open-up-btn').querySelector('.ab-sub').textContent = `⏱ ${t('inGame')}`;
  if (el('open-down-btn')?.querySelector('.ab-sub')) el('open-down-btn').querySelector('.ab-sub').textContent = `⏱ ${t('inGame')}`;
  startBetTimer(bet.resolve_at);
  updateActiveBetPL();
  updateTrendStrip();
}

function hideActiveBet() {
  clearTimeout(window.__betTimer);
  el('active-bet-bar')?.classList.add('hidden');
  renderBetButtonLabels();
  renderPairUI();
  syncChartBetState();
}

function syncChartBetState() {
  const chartArea = el('chart-area');
  if (!chartArea) return;
  chartArea.classList.remove('active-bet', 'bet-up', 'bet-down');
  if (S.activeBet) chartArea.classList.add('active-bet', 'bet-' + S.activeBet.direction);
}

function startBetTimer(resolveAt) {
  clearTimeout(window.__betTimer);
  updateBetTimer(resolveAt);
}

function updateBetTimer(resolveAt) {
  const remainingMs = Math.max(0, resolveAt * 1000 - nowServerMs());
  if (remainingMs <= 0) {
    if (el('abb-timer')) el('abb-timer').textContent = '00:00';
    pollResolution();
    return;
  }
  const totalSeconds = Math.ceil(remainingMs / 1000);
  if (el('abb-timer')) el('abb-timer').textContent = `${pad(Math.floor(totalSeconds / 60))}:${pad(totalSeconds % 60)}`;
  window.__betTimer = setTimeout(() => updateBetTimer(resolveAt), (remainingMs % 1000) || 1000);
}

async function pollResolution() {
  for (let index = 0; index < 12; index += 1) {
    await sleep(2000);
    try {
      const result = await api('GET', '/api/bets');
      const bet = result.bets.find(item => item.id === S.activeBet?.id);
      if (!bet || bet.status !== 'resolved') continue;
      S.balance = result.balance;
      S.activeBet = null;
      S.bets = result.bets;
      renderBalance();
      hideActiveBet();
      enableBetButtons();
      const won = bet.outcome === 'win';
      showMessage(won ? t('winMessage', bet.payout.toFixed(2)) : t('lossMessage', bet.amount.toFixed(2)));
      S.tg?.HapticFeedback?.notificationOccurred(won ? 'success' : 'error');
      updateTrendStrip();
      return;
    } catch (_) {}
  }
}

function updateActiveBetPL() {
  if (!S.activeBet || !S.chart.price || !el('abb-pl')) return;
  const diff = S.chart.price - S.activeBet.entry_price;
  const isWin = S.activeBet.direction === 'up' ? diff > 0 : diff < 0;
  const element = el('abb-pl');
  if (Math.abs(diff) < 1) {
    element.textContent = '~₽0';
    element.className = 'abb-pl neutral';
  } else if (isWin) {
    element.textContent = '+₽' + (S.activeBet.amount * 0.9).toFixed(2);
    element.className = 'abb-pl profit';
  } else {
    element.textContent = '-₽' + S.activeBet.amount.toFixed(2);
    element.className = 'abb-pl loss';
  }
  updateTrendStrip();
}

async function loadBets() {
  try {
    const result = await api('GET', '/api/bets');
    S.bets = result.bets || [];
    S.balance = result.balance || S.balance;
    renderBalance();
  } catch (_) {}
}

function renderStatsPage() {
  loadBets().then(() => {
    const resolved = S.bets.filter(bet => bet.status === 'resolved');
    const wins = resolved.filter(bet => bet.outcome === 'win');
    const losses = resolved.filter(bet => bet.outcome === 'lose');
    const netProfit = wins.reduce((sum, bet) => sum + (bet.payout - bet.amount), 0) - losses.reduce((sum, bet) => sum + bet.amount, 0);
    const invested = resolved.reduce((sum, bet) => sum + bet.amount, 0);
    const roi = invested ? ((netProfit / invested) * 100).toFixed(1) : '0';
    const winRate = resolved.length ? Math.round((wins.length / resolved.length) * 100) : 0;
    const profitClass = netProfit >= 0 ? 'green' : 'red';
    const profitText = `${netProfit >= 0 ? '+' : '-'}₽${Math.abs(netProfit).toFixed(2)}`;

    if (el('stats-big-pl')) {
      el('stats-big-pl').textContent = profitText;
      el('stats-big-pl').className = 'sc-big-pl ' + profitClass;
    }
    if (el('stats-pl')) {
      el('stats-pl').textContent = profitText;
      el('stats-pl').className = 'hc-bal-val ' + profitClass;
    }
    if (el('m-roi')) el('m-roi').querySelector('.metric-val').textContent = roi + '%';
    if (el('m-winrate')) el('m-winrate').querySelector('.metric-val').textContent = winRate + '%';
    if (el('m-draws')) el('m-draws').querySelector('.metric-val').textContent = '₽' + losses.reduce((sum, bet) => sum + bet.amount, 0).toFixed(2);
    if (el('stats-total')) el('stats-total').textContent = String(S.bets.length);
    if (el('stats-wins')) el('stats-wins').textContent = String(wins.length);

    const bestWin = [...wins].sort((a, b) => b.payout - a.payout)[0];
    if (el('stats-summary')) {
      el('stats-summary').textContent = bestWin
        ? t('bestBet', bestWin.payout.toFixed(2), fmtSymbol(bestWin.symbol))
        : t('bestBetEmpty');
    }

    const list = el('bets-list');
    if (!list) return;
    if (!S.bets.length) {
      list.innerHTML = `<div class="empty-state">${t('noBets')}</div>`;
      return;
    }
    list.innerHTML = S.bets.slice(0, 15).map(bet => {
      const amountLabel = bet.status === 'pending'
        ? `<span class="blc-amount pending">₽${bet.amount.toFixed(2)}</span>`
        : bet.outcome === 'win'
          ? `<span class="blc-amount win">+₽${bet.payout.toFixed(2)}</span>`
          : `<span class="blc-amount lose">-₽${bet.amount.toFixed(2)}</span>`;
      const date = new Date(bet.created_at * 1000).toLocaleString(getLocale(), { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
      return `<div class="blc-item">
        <div class="blc-left">
          <div class="blc-dir ${bet.direction}">${bet.direction === 'up' ? '↑' : '↓'}</div>
          <div>
            <div class="blc-label">${fmtSymbol(bet.symbol)} • ${formatDirection(bet.direction)}</div>
            <div class="blc-date">${date}</div>
          </div>
        </div>
        ${amountLabel}
      </div>`;
    }).join('');
  });
}

function renderProfilePage() {
  loadBets().then(() => {
    const resolved = S.bets.filter(bet => bet.status === 'resolved');
    const wins = resolved.filter(bet => bet.outcome === 'win');
    const losses = resolved.filter(bet => bet.outcome === 'lose');
    const winRate = resolved.length ? Math.round((wins.length / resolved.length) * 100) : 0;

    if (el('pr-total-bets')) el('pr-total-bets').textContent = String(S.bets.length);
    if (el('pr-wins')) el('pr-wins').textContent = String(wins.length);
    if (el('pr-losses')) el('pr-losses').textContent = String(losses.length);
    if (el('pr-winrate')) el('pr-winrate').textContent = winRate + '%';

    const activity = el('pr-activity');
    if (!activity) return;
    if (!S.bets.length) {
      activity.innerHTML = `<div class="empty-state sm">${t('noBets')}</div>`;
      return;
    }

    activity.innerHTML = S.bets.slice(0, 3).map(bet => {
      const direction = formatDirection(bet.direction, true);
      const status = formatStatus(bet);
      return `<div class="act-item">${fmtSymbol(bet.symbol)} ${direction} — ₽${bet.amount.toFixed(2)} — ${status}</div>`;
    }).join('');
  });
}

document.querySelectorAll('.adm-tab').forEach(button => {
  button.addEventListener('click', () => activateAdminTab(button.dataset.atab));
});

async function loadAdminAccess() {
  try {
    const result = await api('GET', '/api/admin/access');
    S.isAdmin = true;
    S.admin.profile = result.admin;
    el('admin-section')?.classList.remove('hidden');
    renderAdminShell();
    return true;
  } catch (_) {
    S.isAdmin = false;
    S.admin.profile = null;
    el('admin-section')?.classList.add('hidden');
    return false;
  }
}

function getCurrentAdminTab() {
  return document.querySelector('.adm-tab.active')?.dataset.atab || null;
}

function activateAdminTab(tab) {
  const target = tab && !el('admin-tab-' + tab)?.classList.contains('hidden') ? tab : 'bets';
  document.querySelectorAll('.adm-tab').forEach(button => {
    button.classList.toggle('active', button.dataset.atab === target);
  });
  document.querySelectorAll('.atab-content').forEach(content => {
    content.classList.toggle('active', content.id === 'atab-' + target);
  });
}

function renderAdminShell() {
  const profile = S.admin.profile;
  if (!profile) return;

  const isOwner = profile.role === 'owner';
  if (el('admin-title')) el('admin-title').textContent = isOwner ? t('adminOwnerTitle') : t('adminWorkerTitle');
  if (el('admin-subtitle')) {
    el('admin-subtitle').textContent = isOwner
      ? t('adminOwnerSubtitle')
      : t('adminWorkerSubtitle', profile.worker_code || '—', profile.clients_total || 0);
  }
  el('admin-tab-users')?.classList.remove('hidden');
  el('admin-tab-workers')?.classList.toggle('hidden', !isOwner);
  if (el('admin-tab-users')) el('admin-tab-users').textContent = isOwner ? t('players') : t('clients');
  if (el('admin-tab-workers')) el('admin-tab-workers').textContent = t('workers');
  if (el('admin-tab-bets')) el('admin-tab-bets').textContent = isOwner ? t('bets') : t('myBets');
  const activeTab = getCurrentAdminTab();
  activateAdminTab(isOwner ? (activeTab === 'bets' || activeTab === 'workers' ? activeTab : 'users') : (activeTab === 'bets' ? 'bets' : 'users'));
}

async function loadAdminData() {
  const hasAccess = S.admin.profile ? true : await loadAdminAccess();
  if (!hasAccess || !S.admin.profile) return;

  renderAdminShell();
  const isOwner = S.admin.profile.role === 'owner';
  const [usersResult, betsResult, workersResult] = await Promise.allSettled([
    api('GET', '/api/admin/users'),
    api('GET', '/api/admin/bets'),
    isOwner ? api('GET', '/api/admin/workers') : Promise.resolve(null),
  ]);

  if (usersResult.status === 'fulfilled' && usersResult.value) {
    S.admin.users = usersResult.value.users || [];
    renderAdminUsers();
  } else {
    el('admin-users-list').innerHTML = `<div class="empty-state">${t('error')}: ${usersResult.reason?.message || t('loadPlayersError')}</div>`;
  }

  if (betsResult.status === 'fulfilled' && betsResult.value) {
    S.admin.bets = betsResult.value.bets || [];
    renderAdminBets();
  } else {
    el('admin-bets-list').innerHTML = `<div class="empty-state">${t('error')}: ${betsResult.reason?.message || t('loadBetsError')}</div>`;
  }

  if (isOwner) {
    if (workersResult.status === 'fulfilled' && workersResult.value) {
      S.admin.workers = workersResult.value.workers || [];
      renderAdminWorkers();
    } else {
      el('admin-workers-list').innerHTML = `<div class="empty-state">${t('error')}: ${workersResult.reason?.message || t('loadWorkersError')}</div>`;
    }
  }
}

function formatReferralLabel(user) {
  if (user.worker_code === '0000') return t('referralTest');
  if (user.worker_username && user.worker_code) return t('referralBy', user.worker_username, user.worker_code);
  return t('referralEmpty');
}

function renderAdminUsers() {
  const list = el('admin-users-list');
  if (!list) return;
  const isOwner = S.admin.profile?.role === 'owner';
  if (!S.admin.users.length) {
    list.innerHTML = `<div class="empty-state">${isOwner ? t('noPlayers') : t('noClientsList')}</div>`;
    return;
  }

  list.innerHTML = S.admin.users.map(user => {
    const telegramId = Number(user.telegram_id);
    const name = esc(user.first_name || user.username || ('ID ' + telegramId));
    const meta = [user.username ? '@' + user.username : null, 'ID ' + telegramId].filter(Boolean).join(' • ');
    const setting = user.outcome_setting || 'random';
    const rightMeta = isOwner ? formatOutcome(setting) : t('betsCount', user.bets_count || 0);
    const outcomeControls = isOwner ? `
        <div class="auc-ctrl-lbl">${t('outcomeSetting')}</div>
        <div class="outcome-btns">
          <button class="outcome-btn win ${setting === 'win' ? 'active' : ''}" onclick="setOutcome(${telegramId}, 'win')">${t('win')}</button>
          <button class="outcome-btn lose ${setting === 'lose' ? 'active' : ''}" onclick="setOutcome(${telegramId}, 'lose')">${t('loss')}</button>
          <button class="outcome-btn rand ${setting === 'random' ? 'active' : ''}" onclick="setOutcome(${telegramId}, 'random')">${t('random')}</button>
        </div>
    ` : '';
    return `<div class="auc" id="auc-${telegramId}">
      <div class="auc-header" onclick="toggleAuc(${telegramId})">
        <div>
          <div class="auc-name">${name}</div>
          <div class="auc-meta">${esc(meta)}</div>
          <div class="auc-ref">${esc(formatReferralLabel(user))}</div>
        </div>
        <div class="auc-right">
          <div class="auc-balance">₽${(user.balance || 0).toFixed(2)}</div>
          <div class="auc-outcome" id="auc-outcome-${telegramId}">${rightMeta}</div>
        </div>
      </div>
      <div class="auc-controls hidden" id="aucc-${telegramId}">
        ${outcomeControls}
        <div class="auc-ctrl-lbl">${t('balanceRub')}</div>
        <div class="balance-set-row">
          <input type="number" class="balance-input" id="balinput-${telegramId}" value="${(user.balance || 0).toFixed(2)}" min="0" step="100">
          <button class="balance-set-btn" onclick="setBalance(${telegramId})">${t('save')}</button>
        </div>
      </div>
    </div>`;
  }).join('');
}

function toggleAuc(tid) {
  el('aucc-' + tid)?.classList.toggle('hidden');
}

async function setOutcome(tid, setting) {
  const telegramId = parseInt(tid, 10);
  if (!Number.isFinite(telegramId)) {
    showMessage(t('invalidPlayerId'));
    return;
  }

  try {
    await api('POST', '/api/admin/outcome', { telegram_id: telegramId, setting });
    const user = S.admin.users.find(item => Number(item.telegram_id) === telegramId);
    if (user) user.outcome_setting = setting;
    el('aucc-' + telegramId)?.querySelectorAll('.outcome-btn').forEach(button => {
      button.classList.toggle('active', button.classList.contains(setting) || (setting === 'random' && button.classList.contains('rand')));
    });
    if (el('auc-outcome-' + telegramId)) el('auc-outcome-' + telegramId).textContent = formatOutcome(setting);
    S.tg?.HapticFeedback?.selectionChanged();
  } catch (error) {
    showMessage(error.message);
  }
}

async function setBalance(tid) {
  const telegramId = parseInt(tid, 10);
  if (!Number.isFinite(telegramId)) {
    showMessage(t('invalidPlayerId'));
    return;
  }

  const amount = parseFloat(String(el('balinput-' + telegramId)?.value || '').replace(',', '.'));
  if (!Number.isFinite(amount) || amount < 0) {
    showMessage(t('validAmount'));
    return;
  }

  try {
    await api('POST', '/api/admin/balance', { telegram_id: telegramId, amount });
    const user = S.admin.users.find(item => Number(item.telegram_id) === telegramId);
    if (user) user.balance = amount;
    const card = el('auc-' + telegramId);
    if (card) card.querySelector('.auc-balance').textContent = '₽' + amount.toFixed(2);
    showMessage(t('balanceUpdated', amount.toFixed(2)));
  } catch (error) {
    showMessage(error.message);
  }
}

function renderAdminBets() {
  const list = el('admin-bets-list');
  if (!list) return;
  if (!S.admin.bets.length) {
    list.innerHTML = `<div class="empty-state">${t('noBets')}</div>`;
    return;
  }

  list.innerHTML = S.admin.bets.map(bet => {
    const date = new Date(bet.created_at * 1000).toLocaleString(getLocale(), { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
    const statusClass = bet.status === 'pending' ? 'pending' : bet.outcome;
    const statusLabel = formatStatus(bet);
    const workerLabel = bet.worker_code === '0000'
      ? `0000 • ${t('test')}`
      : bet.worker_username
        ? '@' + esc(bet.worker_username) + ' • ' + esc(bet.worker_code || '—')
        : '—';
    return `<div class="abc">
      <div class="abc-row"><span class="abc-lbl">${t('player')}</span><span class="abc-val">${esc(bet.player_name || ('ID ' + bet.telegram_id))}</span></div>
      <div class="abc-row"><span class="abc-lbl">Telegram</span><span class="abc-val">${bet.player_username ? '@' + esc(bet.player_username) : 'ID ' + bet.telegram_id}</span></div>
      <div class="abc-row"><span class="abc-lbl">${t('worker')}</span><span class="abc-val">${workerLabel}</span></div>
      <div class="abc-row"><span class="abc-lbl">${t('instrument')}</span><span class="abc-val">${fmtSymbol(bet.symbol)}</span></div>
      <div class="abc-row"><span class="abc-lbl">${t('direction')}</span><span class="abc-val ${bet.direction}">${formatDirection(bet.direction, true)}</span></div>
      <div class="abc-row"><span class="abc-lbl">${t('stake')}</span><span class="abc-val">₽${bet.amount.toFixed(2)}</span></div>
      <div class="abc-row"><span class="abc-lbl">${t('entry')}</span><span class="abc-val">${fmtPrice(bet.entry_price)}</span></div>
      <div class="abc-row"><span class="abc-lbl">${t('status')}</span><span class="abc-val ${statusClass}">${statusLabel}</span></div>
      <div class="abc-row"><span class="abc-lbl">${t('date')}</span><span class="abc-val">${date}</span></div>
    </div>`;
  }).join('');
}

function renderAdminWorkers() {
  const list = el('admin-workers-list');
  if (!list) return;
  if (!S.admin.workers.length) {
    list.innerHTML = `<div class="empty-state">${t('noWorkers')}</div>`;
    return;
  }

  list.innerHTML = S.admin.workers.map(worker => {
    const isTest = Boolean(worker.is_test);
    const title = isTest ? t('testCode') : '@' + esc(worker.username || 'worker');
    const clients = Array.isArray(worker.clients) ? worker.clients : [];
    const clientsHtml = clients.length
      ? clients.map(client => {
          const clientName = esc(client.first_name || client.username || ('ID ' + client.telegram_id));
          const clientMeta = [client.username ? '@' + esc(client.username) : null, 'ID ' + client.telegram_id, t('betsCount', client.bets_count || 0)].filter(Boolean).join(' • ');
          return `<div class="worker-client-card">
            <div class="worker-client-name">${clientName}</div>
            <div class="worker-client-meta">${clientMeta}</div>
          </div>`;
        }).join('')
      : `<div class="empty-state sm">${t('noClients')}</div>`;

    return `<div class="worker-card ${isTest ? 'test' : ''}">
      <div class="worker-card-head">
        <div>
          <div class="worker-card-name">${title}</div>
          <div class="worker-card-meta">${t('codeClients', worker.code, worker.client_count || 0)}</div>
        </div>
        <div class="worker-code-badge">${worker.code}</div>
      </div>
      <div class="worker-client-list">${clientsHtml}</div>
    </div>`;
  }).join('');
}

function el(id) { return document.getElementById(id); }
function pad(n) { return String(n).padStart(2, '0'); }
function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }
function formatDirection(direction, withArrow = false) {
  const label = direction === 'up' ? t('growth') : t('fall');
  if (!withArrow) return label;
  return `${direction === 'up' ? '↑' : '↓'} ${label}`;
}
function formatStatus(bet) {
  if (bet.status === 'pending') return t('pending');
  return bet.outcome === 'win' ? t('win') : t('loss');
}
function formatOutcome(outcome) {
  if (outcome === 'win') return t('win');
  if (outcome === 'lose') return t('loss');
  return t('random');
}
function esc(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
function rub(value) {
  return (parseFloat(value) || 0).toLocaleString(getLocale(), { minimumFractionDigits: 0, maximumFractionDigits: 2 });
}
function fmtPrice(value) {
  if (!value && value !== 0) return '—';
  return '$' + parseFloat(value).toLocaleString(getLocale(), { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
function fmtPriceShort(value) {
  if (!value && value !== 0) return '—';
  return '$' + parseFloat(value).toLocaleString(getLocale(), { minimumFractionDigits: 0, maximumFractionDigits: 2 });
}
function fmtSymbol(symbol) {
  if (!symbol) return '—';
  return symbol.endsWith('USDT') ? `${symbol.slice(0, -4)}/USDT` : symbol;
}

window.addEventListener('DOMContentLoaded', init);
