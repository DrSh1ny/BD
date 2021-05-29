create or replace function getLeilaoMensagens(
	p_id bigint
)returns table (
	titulo varchar,
	descricao varchar,
	nome varchar,
	data timestamp
) 
language plpgsql
as $$
declare
begin
	return query
		SELECT mensagem.titulo, mensagem.descricao, pessoa.nome,mensagem.data
		FROM mensagem,pessoa 
		where mensagem.pessoa_id = pessoa.id and mensagem.leilao_id =p_id
		order by mensagem.data;
end;
$$