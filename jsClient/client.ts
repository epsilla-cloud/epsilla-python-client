import axios from 'axios';

class Client {
  private protocol: string;
  private host: string;
  private port: string;
  private baseurl: string;
  private db: string | null;
  private timeout: number;
  private header: object;

  constructor(protocol = 'http', host='localhost', port='8888') {
    this.protocol = protocol;
    this.host = host;
    this.port = port;
    this.baseurl = `${this.protocol}://${this.host}:${this.port}`;
    this.db = null;
    this.timeout = 10;
    this.header = {'Content-type': 'application/json'};
  }

  async checkNetworking() {
    try {
      const response = await axios.get(`${this.baseurl}/`, {timeout: this.timeout});
      if (response.status === 200) {
        console.log(`[INFO] Connected to ${this.host}:${this.port} successfully.`);
      } else {
        throw new Error(`[ERROR] Failed to connect to ${this.host}:${this.port}`);
      }
    } catch (error) {
      console.error(error);
    }
  }

  async welcome() {
    const response = await axios.get(`${this.baseurl}/`, {headers: this.header, timeout: this.timeout});
    return response.status, response.data;
  }
  
  async state() {
    const response = await axios.get(`${this.baseurl}/state`, {headers: this.header, timeout: this.timeout});
    return response.status, response.data;
  }
  
  use_db(db_name: string) {
    this.db = db_name;
  }
  
  async load_db(db_name: string, db_path: string, vector_scale: number | null = null, wal_enabled: boolean | null = null) {
    const data = {"name": db_name, "path": db_path};
    if (vector_scale !== null) {
      data["vectorScale"] = vector_scale;
    }
    if (wal_enabled !== null) {
      data["walEnabled"] = wal_enabled;
    }
    const response = await axios.post(`${this.baseurl}/api/load`, data, {headers: this.header, timeout: this.timeout});
    return response.status, response.data;
  }
  
  async unload_db(db_name: string) {
    const response = await axios.post(`${this.baseurl}/api/${db_name}/unload`, null, {headers: this.header, timeout: this.timeout});
    return response.status, response.data;
  }
  
  async create_table(table_name: string = "MyTable", table_fields: object[] = []) {
    if (this.db === null) {
      throw new Error("[ERROR] Please use_db() first!");
    }
    const data = {"name": table_name, "fields": table_fields};
    const response = await axios.post(`${this.baseurl}/api/${this.db}/schema/tables`, data, {headers: this.header, timeout: this.timeout});
    return response.status, response.data;
  }
  
  async insert(table_name: string = "MyTable", records: object[] = []) {
    if (this.db === null) {
      throw new Error("[ERROR] Please use_db() first!");
    }
    const data = {"table": table_name, "data": records};
    const response = await axios.post(`${this.baseurl}/api/${this.db}/data/insert`, data, {headers: this.header, timeout: this.timeout});
    return response.status, response.data;
  }
  
  async query(table_name: string = "MyTable", query_field: string = "", query_vector: number[] = [], response_fields: string[] = [], limit: number = 1, with_distance: boolean = false) {
    if (this.db === null) {
      throw new Error("[ERROR] Please use_db() first!");
    }
    const data = {"table": table_name, "queryField": query_field, "queryVector": query_vector, "response": response_fields, "limit": limit, "withDistance": with_distance};
    const response = await axios.post(`${this.baseurl}/api/${this.db}/data/query`, data, {headers: this.header, timeout: this.timeout});
    return response.status, response.data;
  }
  
  async get(table_name: string = "MyTable", response_fields: string[] = []) {
    if (this.db === null) {
      throw new Error("[ERROR] Please use_db() first!");
    }
    const data = {"table": table_name, "response": response_fields};
    const response = await axios.post(`${this.baseurl}/api/${this.db}/data/get`, data, {headers: this.header, timeout: this.timeout});
    return response.status, response.data;
  }
  
  async drop_table(table_name: string = "MyTable") {
    if (this.db === null) {
      throw new Error("[ERROR] Please use_db() first!");
    }
    const response = await axios.delete(`${this.baseurl}/api/${this.db}/schema/tables/${table_name}`, {headers: this.header, timeout: this.timeout});
    return response.status, response.data;
  }
  
  async drop_db(db_name: string) {
    const response = await axios.delete(`${this.baseurl}/api/${db_name}/drop`, {headers: this.header, timeout: this.timeout});
    return response.status, response.data;
  }
}