# AI DataBridge

A full-stack application for managing and sharing organization data through Model Context Protocol (MCP) instances. This platform allows you to create secure, shareable MCP endpoints that provide LLMs with controlled access to specific database tables.

## 🚀 Features

- **MCP Instance Management**: Create, view, and delete MCP instances with custom access permissions
- **Category-Based Access Control**: Organize database access by schema categories (Sales, Purchasing, Warehouse, Application)
- **Visual Color Coding**: Cards are color-coded based on the number of allowed table categories
- **OpenAI Integration**: Generate SQL queries using OpenAI's API
- **Database Schema Filtering**: Automatically filter database schemas based on instance permissions
- **Modern UI**: Built with Next.js, shadcn/ui, and Tailwind CSS
- **RESTful API**: FastAPI backend with full CRUD operations

## 📋 Prerequisites

- Python 3.12+
- Node.js 20+
- pnpm (or npm)
- SQL Server database (for database connection)
- OpenAI API key

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **FastMCP** - Model Context Protocol server
- **OpenAI** - SQL query generation
- **pymssql** - SQL Server database connection
- **pandas** - Data manipulation
- **uvicorn** - ASGI server

### Frontend
- **Next.js 16** - React framework
- **TypeScript** - Type safety
- **shadcn/ui** - UI component library
- **Tailwind CSS** - Styling
- **Radix UI** - Accessible component primitives

## 📁 Project Structure

```
EnterpriseAI-hackathon/
├── backend/
│   ├── data/
│   │   ├── mcp.json          # MCP instances storage
│   │   └── __init__.py       # Data loading utilities
│   ├── routers/
│   │   ├── api.py            # REST API endpoints
│   │   └── mcp.py            # MCP server tools
│   ├── database.py           # Database connection & schema building
│   ├── main.py              # FastAPI application entry point
│   └── pyproject.toml       # Python dependencies
│
└── frontend/
    ├── app/
    │   ├── page.tsx         # Main MCP instances page
    │   ├── layout.tsx       # Root layout
    │   └── globals.css      # Global styles
    ├── components/
    │   └── ui/              # shadcn/ui components
    └── package.json         # Node dependencies
```

## 🔧 Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies using `uv` (recommended) or `pip`:
```bash
# Using uv
uv sync

# Or using pip
pip install -r requirements.txt
```

3. Create a `.env` file in the backend directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
DB_SERVER=your_database_server
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

4. Update database connection settings in `database.py` if needed.

5. Run the backend server:
```bash
python main.py
# Or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
pnpm install
# Or
npm install
```

3. Create a `.env.local` file (optional, defaults to localhost:8000):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Run the development server:
```bash
pnpm dev
# Or
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📖 Usage

### Creating an MCP Instance

1. Click on the "Add MCP Server" card in the frontend
2. Fill in the form:
   - **MCP Server Name**: A descriptive name for your instance
   - **Description**: Optional description of what this instance provides
   - **Allowed Tables (Categories)**: Select one or more categories:
     - **Sales**: Customers, Orders, OrderLines, Invoices, InvoiceLines, CustomerTransactions, BuyingGroups, CustomerCategories, SpecialDeals
     - **Purchasing**: Suppliers, PurchaseOrders, PurchaseOrderLines, SupplierCategories, SupplierTransactions
     - **Warehouse**: StockItems, StockItemHoldings, StockItemTransactions, StockGroups, Colors, PackageTypes, ColdRoomTemperatures, VehicleTemperatures
     - **Application**: People, Cities, Countries, StateProvinces, DeliveryMethods, PaymentMethods, TransactionTypes, SystemParameters
3. Click "Add MCP Server" to create the instance

### Using MCP Instances

Each MCP instance provides a unique endpoint URL in the format:
```
https://enterprise-ai.onrender.com/llm/mcp?instance_id={uuid}
```

You can:
- **Copy the endpoint URL** using the copy button on each card
- **Use the endpoint** with MCP Inspector or any MCP-compatible client
- **Delete instances** using the delete button

### MCP Tools

The MCP server provides three tools:

1. **`get_database_context`**: Returns filtered database schema context based on allowed tables
2. **`generate_sql_query`**: Generates SQL queries using OpenAI based on user requests
3. **`execute_query`**: Executes SQL queries on the database

## 🎨 Color Coding

MCP instance cards are color-coded based on the number of allowed table categories:

- **1 category** → Blue
- **2 categories** → Green
- **3 categories** → Purple
- **4 categories** → Amber/Orange
- **5+ categories** → Pink

## 🔌 API Endpoints

### GET `/mcp`
Get all MCP instances

### GET `/mcp/{instance_id}`
Get a specific MCP instance by ID

### POST `/mcp`
Create a new MCP instance
```json
{
  "name": "My MCP Instance",
  "description": "Description here",
  "allowedTables": ["Sales", "Warehouse"]
}
```

### DELETE `/mcp/{instance_id}`
Delete an MCP instance

### MCP Endpoint: `/llm/mcp?instance_id={instance_id}`
Connect to the MCP server with a specific instance ID

## 🔐 Security

- Instance IDs are UUIDs for uniqueness
- Database schema filtering ensures only allowed tables are accessible
- CORS is configured for development (should be restricted in production)
- Each instance has isolated access permissions

## 🚀 Deployment

### Backend (Render/Similar)

1. Set environment variables in your hosting platform
2. Ensure `mcp.json` is persisted (consider using a database in production)
3. Deploy the FastAPI application

### Frontend (Vercel/Similar)

1. Set `NEXT_PUBLIC_API_URL` to your backend URL
2. Deploy the Next.js application

## 📝 Environment Variables

### Backend
- `OPENAI_API_KEY` - Your OpenAI API key
- Database connection variables (configured in `database.py`)

### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL (defaults to `http://localhost:8000`)

## 🤝 Contributing

This is a hackathon project. Feel free to fork and extend!

## 📄 License

This project is part of the Enterprise AI Hackathon.

## 🙏 Acknowledgments

- FastMCP for MCP server implementation
- shadcn/ui for beautiful UI components
- OpenAI for SQL generation capabilities

