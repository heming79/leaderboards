class LeaderboardApp {
    constructor() {
        this.currentTab = 'models';
        this.currentPage = 1;
        this.perPage = 20;
        this.sortBy = 'intelligence_index';
        this.sortOrder = 'desc';
        this.totalPages = 1;
        this.filters = {
            search: '',
            provider_name: '',
            license_type: '',
            is_open_source: null,
            min_context_window: null
        };
        this.filterOptions = {
            providers: [],
            license_types: []
        };
        this.init();
    }

    async init() {
        await this.loadFilterOptions();
        this.bindEvents();
        this.loadCurrentTab();
    }

    async loadFilterOptions() {
        try {
            const response = await fetch('/api/filters/options');
            if (response.ok) {
                this.filterOptions = await response.json();
                this.populateFilterDropdowns();
            }
        } catch (error) {
            console.error('Error loading filter options:', error);
        }
    }

    populateFilterDropdowns() {
        const providerFilter = document.getElementById('providerFilter');
        const licenseFilter = document.getElementById('licenseFilter');

        if (providerFilter && this.filterOptions.providers) {
            const currentValue = providerFilter.value;
            providerFilter.innerHTML = '<option value="">All Providers</option>';
            this.filterOptions.providers.forEach(provider => {
                const option = document.createElement('option');
                option.value = provider;
                option.textContent = provider;
                if (provider === currentValue) option.selected = true;
                providerFilter.appendChild(option);
            });
        }

        if (licenseFilter && this.filterOptions.license_types) {
            const currentValue = licenseFilter.value;
            licenseFilter.innerHTML = '<option value="">All Licenses</option>';
            this.filterOptions.license_types.forEach(license => {
                const option = document.createElement('option');
                option.value = license;
                option.textContent = license;
                if (license === currentValue) option.selected = true;
                licenseFilter.appendChild(option);
            });
        }
    }

    bindEvents() {
        const tabBtns = document.querySelectorAll('.tab-btn');
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                this.switchTab(btn.dataset.tab);
            });
        });

        const sortBySelect = document.getElementById('sortBy');
        const sortOrderSelect = document.getElementById('sortOrder');
        const refreshBtn = document.getElementById('refreshBtn');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const applyFiltersBtn = document.getElementById('applyFiltersBtn');
        const clearFiltersBtn = document.getElementById('clearFiltersBtn');

        sortBySelect.addEventListener('change', () => {
            this.sortBy = sortBySelect.value;
            this.currentPage = 1;
            this.loadCurrentTab();
        });

        sortOrderSelect.addEventListener('change', () => {
            this.sortOrder = sortOrderSelect.value;
            this.currentPage = 1;
            this.loadCurrentTab();
        });

        refreshBtn.addEventListener('click', () => {
            this.loadFilterOptions();
            this.loadCurrentTab();
        });

        prevBtn.addEventListener('click', () => {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.loadCurrentTab();
            }
        });

        nextBtn.addEventListener('click', () => {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
                this.loadCurrentTab();
            }
        });

        if (applyFiltersBtn) {
            applyFiltersBtn.addEventListener('click', () => {
                this.applyFilters();
            });
        }

        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', () => {
                this.clearFilters();
            });
        }

        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.applyFilters();
                }
            });
        }
    }

    switchTab(tab) {
        this.currentTab = tab;
        this.currentPage = 1;

        const tabBtns = document.querySelectorAll('.tab-btn');
        tabBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tab);
        });

        const modelsContainer = document.getElementById('modelsTableContainer');
        const providersContainer = document.getElementById('providersTableContainer');
        const providerFilterGroup = document.getElementById('providerFilterGroup');
        const licenseFilterGroup = document.getElementById('licenseFilterGroup');
        const openSourceFilterGroup = document.getElementById('openSourceFilterGroup');
        const contextWindowGroup = document.getElementById('contextWindowGroup');

        if (tab === 'models') {
            modelsContainer.style.display = 'block';
            providersContainer.style.display = 'none';
            if (providerFilterGroup) providerFilterGroup.style.display = 'flex';
            if (licenseFilterGroup) licenseFilterGroup.style.display = 'flex';
            if (openSourceFilterGroup) openSourceFilterGroup.style.display = 'flex';
            if (contextWindowGroup) contextWindowGroup.style.display = 'flex';
        } else {
            modelsContainer.style.display = 'none';
            providersContainer.style.display = 'block';
            if (providerFilterGroup) providerFilterGroup.style.display = 'none';
            if (licenseFilterGroup) licenseFilterGroup.style.display = 'none';
            if (openSourceFilterGroup) openSourceFilterGroup.style.display = 'none';
            if (contextWindowGroup) contextWindowGroup.style.display = 'none';
        }

        this.loadCurrentTab();
    }

    applyFilters() {
        const searchInput = document.getElementById('searchInput');
        const providerFilter = document.getElementById('providerFilter');
        const licenseFilter = document.getElementById('licenseFilter');
        const openSourceFilter = document.getElementById('openSourceFilter');
        const minContextWindow = document.getElementById('minContextWindow');

        this.filters = {
            search: searchInput ? searchInput.value.trim() : '',
            provider_name: providerFilter ? providerFilter.value : '',
            license_type: licenseFilter ? licenseFilter.value : '',
            is_open_source: openSourceFilter && openSourceFilter.value ? openSourceFilter.value : null,
            min_context_window: minContextWindow && minContextWindow.value ? parseInt(minContextWindow.value) : null
        };

        this.currentPage = 1;
        this.loadCurrentTab();
    }

    clearFilters() {
        const searchInput = document.getElementById('searchInput');
        const providerFilter = document.getElementById('providerFilter');
        const licenseFilter = document.getElementById('licenseFilter');
        const openSourceFilter = document.getElementById('openSourceFilter');
        const minContextWindow = document.getElementById('minContextWindow');

        if (searchInput) searchInput.value = '';
        if (providerFilter) providerFilter.value = '';
        if (licenseFilter) licenseFilter.value = '';
        if (openSourceFilter) openSourceFilter.value = '';
        if (minContextWindow) minContextWindow.value = '';

        this.filters = {
            search: '',
            provider_name: '',
            license_type: '',
            is_open_source: null,
            min_context_window: null
        };

        this.currentPage = 1;
        this.loadCurrentTab();
    }

    loadCurrentTab() {
        if (this.currentTab === 'models') {
            this.loadModels();
        } else {
            this.loadProviders();
        }
    }

    async loadModels() {
        const tableBody = document.getElementById('modelsTableBody');
        tableBody.innerHTML = '<tr><td colspan="16" class="loading">Loading data...</td></tr>';

        try {
            let url = `/api/models?page=${this.currentPage}&per_page=${this.perPage}&sort_by=${this.sortBy}&sort_order=${this.sortOrder}`;
            
            if (this.filters.search) {
                url += `&search=${encodeURIComponent(this.filters.search)}`;
            }
            if (this.filters.provider_name) {
                url += `&provider_name=${encodeURIComponent(this.filters.provider_name)}`;
            }
            if (this.filters.license_type) {
                url += `&license_type=${encodeURIComponent(this.filters.license_type)}`;
            }
            if (this.filters.is_open_source !== null && this.filters.is_open_source !== '') {
                url += `&is_open_source=${this.filters.is_open_source}`;
            }
            if (this.filters.min_context_window) {
                url += `&min_context_window=${this.filters.min_context_window}`;
            }

            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error('Failed to load models');
            }

            const data = await response.json();
            this.totalPages = data.pages;
            this.renderModels(data.models);
            this.updatePagination();
        } catch (error) {
            console.error('Error loading models:', error);
            tableBody.innerHTML = '<tr><td colspan="16" class="loading">Error loading data. Please try again.</td></tr>';
        }
    }

    async loadProviders() {
        const tableBody = document.getElementById('providersTableBody');
        tableBody.innerHTML = '<tr><td colspan="11" class="loading">Loading data...</td></tr>';

        try {
            let url = `/api/providers?page=${this.currentPage}&per_page=${this.perPage}&sort_by=${this.sortBy}&sort_order=${this.sortOrder}`;
            
            if (this.filters.search) {
                url += `&search=${encodeURIComponent(this.filters.search)}`;
            }

            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error('Failed to load providers');
            }

            const data = await response.json();
            this.totalPages = data.pages;
            this.renderProviders(data.providers);
            this.updatePagination();
        } catch (error) {
            console.error('Error loading providers:', error);
            tableBody.innerHTML = '<tr><td colspan="11" class="loading">Error loading data. Please try again.</td></tr>';
        }
    }

    renderModels(models) {
        const tableBody = document.getElementById('modelsTableBody');
        
        if (models.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="16" class="loading">No models found.</td></tr>';
            return;
        }

        let html = '';
        models.forEach((model, index) => {
            const rank = (this.currentPage - 1) * this.perPage + index + 1;
            html += `
                <tr>
                    <td class="rank">${rank}</td>
                    <td class="logo-cell">${this.renderLogo(model.provider_name, model.logo_url)}</td>
                    <td class="model-name">${this.escapeHtml(model.name)}</td>
                    <td class="provider-name">${this.escapeHtml(model.provider_name || '-')}</td>
                    <td class="${this.getScoreClass(model.intelligence_index)}">${this.formatNumber(model.intelligence_index)}</td>
                    <td class="${this.getScoreClass(model.coding_index)}">${this.formatNumber(model.coding_index)}</td>
                    <td class="${this.getScoreClass(model.agentic_index)}">${this.formatNumber(model.agentic_index)}</td>
                    <td class="context-window">${this.formatContextWindow(model.context_window)}</td>
                    <td>${this.renderLicenseBadge(model.license_type)}</td>
                    <td>${this.renderOpenSourceBadge(model.is_open_source)}</td>
                    <td class="model-size">${this.escapeHtml(model.model_size || '-')}</td>
                    <td>$${this.formatPrice(model.price_per_1k_input)}</td>
                    <td>$${this.formatPrice(model.price_per_1k_output)}</td>
                    <td>${this.formatNumber(model.latency_ms)}</td>
                    <td>${this.formatNumber(model.throughput_tokens_per_sec)}</td>
                </tr>
            `;
        });

        tableBody.innerHTML = html;
    }

    renderProviders(providers) {
        const tableBody = document.getElementById('providersTableBody');
        
        if (providers.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="11" class="loading">No providers found.</td></tr>';
            return;
        }

        let html = '';
        providers.forEach((provider, index) => {
            const rank = (this.currentPage - 1) * this.perPage + index + 1;
            html += `
                <tr>
                    <td class="rank">${rank}</td>
                    <td class="logo-cell">${this.renderLogo(provider.name, provider.logo_url)}</td>
                    <td class="provider-name">${this.escapeHtml(provider.name)}</td>
                    <td class="${this.getScoreClass(provider.intelligence_index)}">${this.formatNumber(provider.intelligence_index)}</td>
                    <td class="${this.getScoreClass(provider.coding_index)}">${this.formatNumber(provider.coding_index)}</td>
                    <td class="${this.getScoreClass(provider.agentic_index)}">${this.formatNumber(provider.agentic_index)}</td>
                    <td>$${this.formatPrice(provider.price_per_1k_input)}</td>
                    <td>$${this.formatPrice(provider.price_per_1k_output)}</td>
                    <td>${this.formatNumber(provider.latency_ms)}</td>
                    <td>${this.formatNumber(provider.throughput_tokens_per_sec)}</td>
                    <td>${provider.models_count || '-'}</td>
                </tr>
            `;
        });

        tableBody.innerHTML = html;
    }

    renderLogo(name, logoUrl) {
        if (logoUrl) {
            return `<img src="${this.escapeHtml(logoUrl)}" alt="${this.escapeHtml(name)}" class="provider-logo" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                    <div class="logo-placeholder" style="display: none;">${this.getInitials(name)}</div>`;
        }
        return `<div class="logo-placeholder">${this.getInitials(name)}</div>`;
    }

    getInitials(name) {
        if (!name) return '?';
        return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
    }

    renderLicenseBadge(licenseType) {
        if (!licenseType) return '-';
        
        let badgeClass = 'license-proprietary';
        const licenseLower = licenseType.toLowerCase();
        
        if (licenseLower.includes('apache')) {
            badgeClass = 'license-apache';
        } else if (licenseLower.includes('mit')) {
            badgeClass = 'license-mit';
        } else if (licenseLower.includes('llama')) {
            badgeClass = 'license-llama';
        } else if (licenseLower.includes('open') || licenseLower.includes('source')) {
            badgeClass = 'license-open';
        }
        
        return `<span class="license-badge ${badgeClass}">${this.escapeHtml(licenseType)}</span>`;
    }

    renderOpenSourceBadge(isOpenSource) {
        if (isOpenSource === null || isOpenSource === undefined) return '-';
        
        const badgeClass = isOpenSource ? 'open-source-yes' : 'open-source-no';
        const text = isOpenSource ? 'Yes' : 'No';
        
        return `<span class="open-source-badge ${badgeClass}">${text}</span>`;
    }

    formatContextWindow(contextWindow) {
        if (contextWindow === null || contextWindow === undefined) return '-';
        
        if (contextWindow >= 1000000) {
            return (contextWindow / 1000000).toFixed(1) + 'M';
        } else if (contextWindow >= 1000) {
            return (contextWindow / 1000).toFixed(0) + 'K';
        }
        return contextWindow.toString();
    }

    updatePagination() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const pageInfo = document.getElementById('pageInfo');

        prevBtn.disabled = this.currentPage <= 1;
        nextBtn.disabled = this.currentPage >= this.totalPages;
        pageInfo.textContent = `Page ${this.currentPage} of ${this.totalPages}`;
    }

    getScoreClass(score) {
        if (score === null || score === undefined) return '';
        if (score >= 90) return 'high-score';
        if (score >= 70) return 'medium-score';
        return 'low-score';
    }

    formatNumber(num) {
        if (num === null || num === undefined) return '-';
        return Number(num).toFixed(1);
    }

    formatPrice(price) {
        if (price === null || price === undefined) return '-';
        return Number(price).toFixed(5);
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new LeaderboardApp();
});
