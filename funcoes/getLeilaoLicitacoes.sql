create or replace function getLeilaoLicitacoes(
	p_id bigint
)returns table (
		precoLicitacao bigint,
		nomePessoa varchar,
		dataLicitacao timestamp
) 
language 'plpgsql'
as $$
declare
begin
	return query
		SELECT licitacao.preco, pessoa.nome, licitacao.data
		FROM licitacao, pessoa 
		where  licitacao.pessoa_id = pessoa.id and leilao_id = p_id
		order by licitacao.data;
end;
$$