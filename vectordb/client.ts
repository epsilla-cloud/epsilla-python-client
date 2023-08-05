import axios from 'axios';

interface ClientConfig {
  protocol?: string;
  host?: string;
  port?: string;
}

class Client {
  private protocol: string;
  private host: string;
  private port: string;
  private baseurl: string;
  private db: string | null;
  private timeout: number;
  private headers: { 'Content-type': string };

  constructor({ protocol = 'http', host = 'localhost', port = '8888' }: ClientConfig = {}) {
    this.protocol = protocol;
    this.host = host;
    this.port = port;
    this.baseurl = `${this.protocol}://${this.host}:${this.port}`;
    this.db = null;
    this.timeout = 10;
    this.headers = { 'Content-type': 'application/json' };
    this.checkNetworking();
  }

  private async checkNetworking() {
    try {
      const response = await axios.get(`${this.baseurl}/`, { timeout: this.timeout });
      if (response.status === 200) {
        console.log(`[INFO] Connected to ${this.host}:${this.port} successfully.`);
      } else {
        throw new Error(`[ERROR] Failed to connect to ${this.host}:${this.port}`);
      }
    } catch (error) {
      throw new Error(`[ERROR] Failed to connect to ${this.host}:${this.port}`);
    }
  }

  async welcome() {
    const response = await axios.get(`${this.baseurl}/`, { headers: this.headers, timeout: this.timeout });
    return response.status, response.data;
  }

  async state() {
    const response = await axios.get(`${this.baseurl}/state`, { headers: this.headers, timeout: this.timeout });
    return response.status, response.data;
  }

  use_db(db_name: string) {
    this.db = db_name;
  }

  async load_db(db_name: string, db_path: string, vector_scale?: number, wal_enabled?: boolean) {
    const response = await axios.post(`${this.baseurl}/api/load`, { name: db_name, path: db_path, vectorScale: vector_scale, walEnabled: wal_enabled }, { headers: this.headers, timeout: this.timeout });
    return response.status, response.data;
  }

  async unload_db(db_name: string) {
    const response = await axios.post(`${this.baseurl}/api/unload`, { name: db_name }, { headers: this.headers, timeout: this.timeout });
    return response.status, response.data;
  }

  async create_table(table_name: string, fields: any[]) {
    const response = await axios.post(`${this.baseurl}/api/table/create`, { name: table_name, fields: fields }, { headers: this.headers, timeout: this.timeout });
    return response.status, response.data;
  }

  async insert(table_name: string, records: any[]) {
    const response = await axios.post(`${this.baseurl}/api/insert`, { name: table_name, records: records }, { headers: this.headers, timeout: this.timeout });
    return response.status, response.data;
  }

  async query(table_name: string, topk: number, query: any) {
    const response = await axios.post(`${this.baseurl}/api/query`, { name: table_name, topk: topk, query: query }, { headers: this.headers, timeout: this.timeout });
    return response.status, response.data;
  }

  async get(table_name: string, ids: any[]) {
    const response = await axios.post(`${this.baseurl}/api/get`, { name: table_name, ids: ids }, { headers: this.headers, timeout: this.timeout });
    return response.status, response.data;
  }

  async drop_table(table_name: string) {
    const response = await axios.post(`${this.baseurl}/api/table/drop`, { name: table_name }, { headers: this.headers, timeout: this.timeout });
    return response.status, response.data;
  }

  async drop_db(db_name: string) {
    const response = await axios.post(`${this.baseurl}/api/drop`, { name: db_name }, { headers: this.headers, timeout: this.timeout });
    return response.status, response.data;
  }
}