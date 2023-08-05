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

  // Add the remaining methods `unload_db`, `create_table`, `insert`, `query`, `get`, `drop_table`, and `drop_db` here, following the same structure and logic as in the Python client
}