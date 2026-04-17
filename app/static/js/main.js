class LeaderboardApp {
    constructor() {
        this.currentPage = 1;
        this.perPage = 20;
        this.sortBy = 'intelligence_index';
        this.sortOrder = 'desc';
        this.totalPages = 1;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadProviders();
    }

    bindEvents() {
        const sortBySelect = document.getElementById('sortBy');
        const sortOrderSelect = document.getElementById('sortOrder');
        const refreshBtn = document.getElementById('refreshBtn');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');

        sortBySelect.addEventListener('change', () => {
            this.sortBy = sortBySelect.value;
            this.currentPage = 1;
            this.loadProviders();
        });

        sortOrderSelect.addEventListener('change', () => {
            this.sortOrder = sortOrderSelect.value;
            this.currentPage = 1;
            this.loadProviders();
        });

        refreshBtn.addEventListener('click', () => {
            this.loadProviders();
        });

        prevBtn.addEventListener('click', () => {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.loadProviders();
            }
        });

        nextBtn.addEventListener('click', () => {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
                this.loadProviders();
            }
        });
    }

    async loadProviders() {
        const tableBody = document.getElementById('providerTableBody');
        tableBody.innerHTML = '<tr><td colspan="10" class="loading">Loading data...</td></tr>';

        try {
            const url = `/api/providers?page=${this.currentPage}&per_page=${this.perPage}&sort_by=${this.sortBy}&sort_order=${this.sortOrder}`;
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
            tableBody.innerHTML = '<tr><td colspan="10" class="loading">Error loading data. Please try again.</td></tr>';
        }
    }

    renderProviders(providers) {
        const tableBody = document.getElementById('providerTableBody');
        
        if (providers.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="10" class="loading">No providers found.</td></tr>';
            return;
        }

        let html = '';
        providers.forEach((provider, index) => {
            const rank = (this.currentPage - 1) * this.perPage + index + 1;
            html += `
                <tr>
                    <td class="rank">${rank}</td>
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
        return Number(price).toFixed(4);
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
