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

  // Rest of the methods go here, mirroring the functionality of the Python Client class
}