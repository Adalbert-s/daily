using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TodoApi.Models;

namespace TodoApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TodoNotaController : ControllerBase
    {
        private readonly TodoContext _context;

        public TodoNotaController(TodoContext context)
        {
            _context = context;
        }

        // GET: api/TodoNota
        [HttpGet]
        public async Task<ActionResult<IEnumerable<TodoNota>>> GetTodoNotas()
        {
            if (_context.TodoNotas == null)
            {
                return NotFound();
            }

            return await _context.TodoNotas.ToListAsync();
        }

        // GET: api/TodoNota/5
        [HttpGet("{id}")]
        public async Task<ActionResult<TodoNota>> GetTodoNota(int id)
        {
            var todoNota = await _context.TodoNotas.FindAsync(id);

            if (todoNota == null)
            {
                return NotFound();
            }

            return todoNota;
        }

        // POST: api/TodoNota
        [HttpPost]
        public async Task<ActionResult<TodoNota>> PostTodoNota(TodoNota todoNota)
        {
            _context.TodoNotas.Add(todoNota);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetTodoNota), new { id = todoNota.Id }, todoNota);
        }

        // PUT: api/TodoNota/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutTodoNota(int id, TodoNota todoNota)
        {
            if (id != todoNota.Id)
            {
                return BadRequest();
            }

            _context.Entry(todoNota).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!TodoNotaExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // DELETE: api/TodoNota/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteTodoNota(int id)
        {
            var todoNota = await _context.TodoNotas.FindAsync(id);
            if (todoNota == null)
            {
                return NotFound();
            }

            _context.TodoNotas.Remove(todoNota);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool TodoNotaExists(int id)
        {
            return _context.TodoNotas.Any(e => e.Id == id);
        }
    }

}
